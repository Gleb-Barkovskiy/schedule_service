import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.api_v1.schedule.crud import course_crud, group_crud, lesson_crud


async def fetch_html(url: str) -> BeautifulSoup:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")


async def parse_main_page(url):
    soup = await fetch_html(url)
    content_area = soup.find("section", class_="content-area default-format")
    if not content_area:
        raise ValueError("Section with class 'content-area default-format' not found.")

    links = []
    a_count = 0
    for a_tag in content_area.find_all("a"):
        if a_count >= 4:  # Stop after 4 courses
            break
        title = a_tag.text.strip().split(" ")[0]
        links.append({"course": title, "url": a_tag["href"]})
        a_count += 1

    return links


async def parse_nested_links(links):
    updated_links = []
    for link_info in links:
        course_title = link_info["course"]
        course_url = link_info["url"]
        soup = await fetch_html(course_url)

        content_area = soup.find("section", class_="content-area default-format")
        if not content_area:
            continue

        groups = []
        for a_tag in content_area.find_all("a"):
            title = a_tag.text.strip().split(" ")[0]
            groups.append({"group": title, "url": a_tag["href"]})

        updated_links.append({"course": course_title, "groups": groups})

    return updated_links


async def parse_schedule_table(link_info):
    for group in link_info.get("groups", []):
        group_url = group["url"]
        soup = await fetch_html(group_url)  # Ensure fetch_html is async
        table = soup.find("table")
        if not table:
            continue

        # Remove the first row if it exists (header row)
        first_row = table.find("tr")
        if first_row:
            first_row.decompose()

        schedule = []
        for tr in table.find_all("tr"):
            subject_teachers = tr.find("td", class_="subject-teachers")
            subject = teacher = None

            if subject_teachers:
                parts = subject_teachers.contents
                if len(parts) == 3:  # Typical case: "Subject - Teacher"
                    subject = parts[0].strip()
                    teacher = parts[2].strip()
                else:
                    subject_teachers_text = subject_teachers.text.strip()
                    if subject_teachers_text.startswith("Физическая"):  # Specific handling for this case
                        subject = subject_teachers_text
                        teacher = None
                    else:
                        subject = subject_teachers_text
                        teacher = None

            row = {
                "weekday": tr.find("td", class_="weekday").text.strip() if tr.find("td", class_="weekday") else "",
                "time": tr.find("td", class_="time").text.strip() if tr.find("td", class_="time") else "",
                "remarks": tr.find("td", class_="remarks").text.strip() if tr.find("td", class_="remarks") else "",
                "subject": subject,
                "teacher": teacher,
                "lecture_practice": tr.find("td", class_="lecture-practice").text.strip()
                if tr.find("td", class_="lecture-practice")
                else "",
                "room": tr.find("td", class_="room").text.strip() if tr.find("td", class_="room") else "",
            }
            schedule.append(row)

        group["schedule"] = schedule

        del group["url"]


async def insert_data_to_db(data, session: AsyncSession):
    for course_data in data:
        course = await course_crud.create(session, {"course_number": course_data["course"]})

        for group_data in course_data.get("groups", []):
            group = await group_crud.create(session, {
                "course_id": course.id,
                "group_number": group_data["group"]
            })

            for lesson_data in group_data.get("schedule", []):
                await lesson_crud.create(session, {
                    "course_id": course.id,
                    "group_id": group.id,
                    "weekday": lesson_data["weekday"],
                    "time": lesson_data["time"],
                    "subject": lesson_data["subject"],
                    "teacher": lesson_data["teacher"],
                    "lecture_practice": lesson_data["lecture_practice"],
                    "room": lesson_data["room"],
                    "remarks": lesson_data["remarks"],
                })


async def scrape_and_populate():
    main_url = "https://mmf.bsu.by/ru/raspisanie-zanyatij/"
    links = await parse_main_page(main_url)
    updated_links = await parse_nested_links(links)

    for link_info in updated_links:
        await parse_schedule_table(link_info)

    async with db_helper.session_factory() as session:
        try:
            await insert_data_to_db(updated_links, session)
            print("Database populated successfully.")
        except Exception as e:
            print(f"Error during database population: {e}")
