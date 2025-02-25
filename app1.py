from flask import Flask, render_template_string, request
import os
import pandas as pd

app = Flask(__name__)

home_page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Transorbital Week</title>
  <style>
    /* Reset and basic styling */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; padding-bottom: 100px; }
    header { background-color: darkgoldenrod; color: #fff; padding: 20px; text-align: center; }
    nav { background-color: darkgoldenrod; }
    nav ul { list-style: none; display: flex; justify-content: center; }
    nav ul li { margin: 0 15px; }
    nav ul li a { color: #fff; text-decoration: none; padding: 10px; display: block; }
    nav ul li a:hover { background-color: goldenrod; }
    .container { max-width: 1000px; margin: 20px auto; padding: 20px; background: #fff; border-radius: 5px; }
    .section { margin-bottom: 30px; padding: 20px; }
    /* Course section: left aligned */
    .course-section { text-align: left; }
    .course-title { font-size: 1.4em; margin-bottom: 10px; }
    .course-detail { font-size: 1em; margin: 5px 0; }
    /* Event Schedule section */
    .event-schedule h2 { margin-bottom: 15px; }
    /* Speakers section */
    .speakers { display: flex; gap: 20px; flex-wrap: wrap; }
    .speakers h2 { margin-bottom: 15px; }
    .speaker { text-align: center; }
    .speaker img { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; }
    .sponsor-logo { position: fixed; bottom: 10px; right: 10px; transform: scale(0.33); transform-origin: bottom right; }
    footer { text-align: center; padding: 10px; background-color: darkgoldenrod; color: #fff; margin-top: 20px; }
  </style>
</head>
<body>
  <header>
    <h1>Transorbital Week</h1>
    <p>Welcome to Transorbital Week 2025!</p>
  </header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>
  <div class="container">
    <!-- Course Section -->
    <section id="course" class="section course-section">
      <p class="course-title"><b>Course</b></p>
      <p class="course-detail">Monday-Thursday: Live surgery 1-2 cases at Samsung Medical Center or Asan Medical Center, Seoul, Korea</p>
      <p class="course-detail">Friday: Cadaver dissection</p>
      <p class="course-detail">Registration fee: free</p>
    </section>
    <!-- Event Schedule Section -->
    <section id="event-schedule" class="section event-schedule">
      <h2>Event Schedule</h2>
      <p>The event will be held from March 9-13, 2025 at Samsung Medical Center and Asan Medical Center, Seoul, Korea.</p>
    </section>
    <!-- Featured Speakers Section -->
    <section id="speakers" class="section speakers">
      <h2>Featured Speakers</h2>
      <div class="speaker">
        <a href="/speaker/doosik_kong">
          <img src="http://www.samsunghospital.com/upload/deptdoctors/1679385221440_0937118.jpg" alt="Doo-Sik Kong">
          <p>Doo-Sik Kong</p>
        </a>
      </div>
      <div class="speaker">
        <a href="/speaker/changki_hong">
          <img src="https://asanwonwoo.amc.seoul.kr/asan/file/imageView.do?fileId=F000000567415_OZoiOi" alt="Chang-Ki Hong">
          <p>Chang-Ki Hong</p>
        </a>
      </div>
    </section>
  </div>
  <img class="sponsor-logo" src="https://www.stryker.com/etc/designs/stryker/images/header/logo.png" alt="Stryker Logo">
  <footer>
    <p>&copy; 2025 Transorbital Week. All Rights Reserved.</p>
  </footer>
</body>
</html>
"""

about_page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>About - Transorbital Week</title>
  <style>
    body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
    .content-container { max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 5px; }
    a { color: darkgoldenrod; text-decoration: none; }
  </style>
</head>
<body>
  <div class="content-container">
    <h1>About the Workshop</h1>
    <p>
      Join our intensive workshop designed to master the art and fundamentals of transorbital surgery. From Monday to Thursday, you'll observe 1-2 live surgeries daily at the renowned Samsung Medical Center or Asan Medical Center in Seoul, Korea—offering an exclusive glimpse into advanced surgical techniques and a solid grounding in transorbital surgery principles. On Friday, enhance your skills further through a hands-on cadaver dissection session, which provides the perfect opportunity to refine your technique and confirm core concepts. Best of all, there is no registration fee, making this workshop an unparalleled opportunity for aspiring transorbital surgeons.
    </p>
    <p><a href="/">Return Home</a></p>
  </div>
</body>
</html>
"""

contact_form = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Contact - Transorbital Week</title>
  <style>
    body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
    .form-container { max-width: 500px; margin: auto; background: #fff; padding: 20px; border-radius: 5px; }
    label { display: block; margin-top: 10px; }
    input[type="text"], input[type="email"] { width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 3px; }
    input[type="submit"] { margin-top: 15px; padding: 10px 15px; background-color: darkgoldenrod; color: #fff; border: none; border-radius: 3px; cursor: pointer; }
    input[type="submit"]:hover { background-color: goldenrod; }
  </style>
</head>
<body>
  <div class="form-container">
    <h2>Contact Us</h2>
    <form method="POST" action="/contact">
      <label for="name">Name:</label>
      <input type="text" id="name" name="name" required>
      
      <label for="affiliation">Affiliation:</label>
      <input type="text" id="affiliation" name="affiliation" required>
      
      <label for="country">Country:</label>
      <input type="text" id="country" name="country" required>
      
      <label for="email">Email Address:</label>
      <input type="email" id="email" name="email" required>
      
      <input type="submit" value="Submit">
    </form>
  </div>
</body>
</html>
"""

doosik_kong_page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Doo-Sik Kong - Speaker Profile</title>
  <style>
    body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
    .content-container { max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 5px; }
    a { color: darkgoldenrod; text-decoration: none; }
  </style>
</head>
<body>
  <div class="content-container">
    <h1>Doo-Sik Kong</h1>
    <p>Doo-Sik Kong is a world-renowned neurosurgeon and expert in transorbital surgery, with decades of experience in advanced surgical procedures. His pioneering work in the field has significantly contributed to the evolution of minimally invasive surgical techniques. Dr. Kong is known for his innovative approach, extensive research, and dedication to training the next generation of surgeons. His insights and expertise have earned him international acclaim, making him a highly sought-after speaker and mentor in the field of transorbital surgery.</p>
    <p><a href="/">Return Home</a></p>
  </div>
</body>
</html>
"""

changki_hong_page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chang-Ki Hong - Speaker Profile</title>
  <style>
    body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
    .content-container { max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 5px; }
    a { color: darkgoldenrod; text-decoration: none; }
  </style>
</head>
<body>
  <div class="content-container">
    <h1>Chang-Ki Hong</h1>
    <p>Chang-Ki Hong is a distinguished surgeon recognized for his significant contributions to the field of transorbital surgery. With extensive experience in both clinical practice and academic research, Dr. Hong is renowned for his skill in live surgical demonstrations and his commitment to advancing medical knowledge. His work has inspired many in the surgical community, and he continues to be a leading voice in innovative surgical techniques and patient care.</p>
    <p><a href="/">Return Home</a></p>
  </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_page_html)

@app.route('/about')
def about():
    return render_template_string(about_page_html)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        affiliation = request.form.get('affiliation')
        country = request.form.get('country')
        email = request.form.get('email')
        
        data = {
            "Name": [name],
            "Affiliation": [affiliation],
            "Country": [country],
            "Email Address": [email]
        }
        df_new = pd.DataFrame(data)
        file_path = "contacts.xlsx"
        if os.path.exists(file_path):
            try:
                df_existing = pd.read_excel(file_path)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            except Exception:
                df_combined = df_new
        else:
            df_combined = df_new
        df_combined.to_excel(file_path, index=False)
        return """
        <h2>Thank you for your submission!</h2>
        <p><a href="/">Return Home</a></p>
        """
    return render_template_string(contact_form)

@app.route('/speaker/doosik_kong')
def doosik_kong():
    return render_template_string(doosik_kong_page_html)

@app.route('/speaker/changki_hong')
def changki_hong():
    return render_template_string(changki_hong_page_html)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
