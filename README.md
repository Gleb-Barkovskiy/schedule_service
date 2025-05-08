<h1>Schedule Parser API</h1>
<h3>Parser which parsing schedule for the BSU MMF students from our faculty website </h3>
<p>Project is created with FastAPI, data storage is built via sqlite3 and aiosqlite lib, parsing via bs4 lib.</p>
<p>Schedule updates each 12 hours</p>
<hr>
<p>Endpoints: <br></p>
<ul>
  <li><code>/api/v1/schedule</code> - returns MMF courses data</li>
  <li><code>/api/v1/schedule/{courseID}</code> - returns course groups data</li>
  <li><code>/api/v1/schedule/{courseID}/{groupID}?weekday="Понедельник"</code> - returns group schedule <br> (if weekday specified it returns schedule for a specified day)</li>
</ul>
<p>Telegram bot is in development</p>
