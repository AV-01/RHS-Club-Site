import csv
from pathlib import Path
import os
import pandas as pd
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
import urllib.request
from werkzeug.utils import secure_filename
import shutil
import re
from datetime import datetime, timezone

app = Flask(  # Create a flask app
    __name__)

app = Flask(__name__)  # Create an Instance

UPLOAD_FOLDER = 'static/icons/'
app.secret_key = "cairocoders-ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def trim_newlines(filename):
    with open(filename, "r") as f:
        contents = f.read()
    trimmed_contents = contents.strip()
    with open(filename, "w") as f:
        f.write(trimmed_contents)

def delete_real_row(csv_file, row_number):
    with open(csv_file, "r", newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = []
        for i, row in enumerate(reader):
            if i != row_number:
                rows.append(row)
        with open(csv_file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)


def quick_create_explore():
    Func = open("templates/explore.html", "w")
    html_template = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>RHS Clubs</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
  <link href="/static/css/style.css" rel="stylesheet" type="text/css" />
</head>

<body>
  <!-- This is all the Navbar stuff: -->
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">RHS Clubs</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" href="home">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="explore">Explore</a>
          </li>
          <li class="nav-ite">
            <a class="nav-link" href="#">Calendar</a>
          </li>
        </ul>
        <form class="d-flex" role="search">
          <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>
    </div>
  </nav>
  <!-- All the main part of the body -->
  <header class="page-header header container-fluid">

    <h1 class="text-center mt-5">Our Clubs</h1>
  """
    Func.write(html_template)
    df = pd.read_csv("static/data/club-data.csv")
    # df['id'] = df['id'].str.replace("%2F", "/")
    df['name'] = df['name'].str.replace("%2f", "/")
    for i in df.category.unique():
        category_start_create = f"""
<div class="container mt-3 mt-lg-5">
  <h5>{i}</h5>
    <div class="row pt-3 px-md-2 px-lg-4 row-cols-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-3 g-md-5">
    """
        Func.write(category_start_create)
        df_category = df[df.category == i]
        for x in df_category.index:
            Func.write(f"""
      <div class="col">
          <div class="card shadow-sm rounded-3 h-100" style="border:0px">
            <div class="card-body p-0 alignment-placeholder"></div>
            <div class="position-relative bg-white rounded-3">
              <img src="{df_category['img'][x]}" class="card-img-top" style="max-width:280px;max-height:280px">
              <div class="position-absolute bottom-0 end-0">

              </div>
            </div>
            <div class="card-body p-0 alignment-placeholder bg-silver"></div>
            <div class="card-body p-2 bg-silver">

              <h6 class="card-title">{df_category['name'][x]}</h6>
                <p class="card-text text-truncate">{df_category['desc'][x]}
                </p>
                <a href="/view/{df_category['id'][x]}" class="btn btn-primary mt-auto">Learn more</a>
            </div>
            <div class="card-footer bg-silver">
              <small class="text-muted card-time" data-set-time="{df_category['time-update'][x]}"></small>
            </div>
          </div>
        </div>
        """)
        closing_div = """
    </div>
    </div>
    """
        Func.write(closing_div)
    closing_code = """
  </header>

  <div class="container mt-5">
    <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
      <p class="col-md-4 mb-0 text-muted">Questions? Email <b>aryavratmishra007@gmail.com</b></p>

      <ul class="nav col-md-4 justify-content-end">
        <li class="nav-item"><a href="/" class="nav-link px-2 text-muted">Home</a></li>
        <li class="nav-item"><a href="/explore" class="nav-link px-2 text-muted">Explore</a></li>
        <li class="nav-item"><a href="/calendar" class="nav-link px-2 text-muted">Calendar</a></li>
        <li class="nav-item">
          <p class="nav-link px-2 text-decoration-none opacity-75">Credit: Aryavrat Mishra and Manas Sana</p>
        </li>
      </ul>
    </footer>
  </div>

  <script src="https://code.jquery.com/jquery-3.5.1.min.js"
    integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
  <script src="static/scripts/explore-script.js?v=1"></script>
</body>

</html>
"""
    Func.write(closing_code)
    Func.close()

def edit_website(club_id):
    real_path = f"static/data/{club_id}"
    Func = open(f"templates/{club_id}-edit.html", "w")
    all_data = []
    with open(f"{real_path}/{club_id}.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    club_basic_data = all_data[1:][0]
    club_slogan = ""
    with open(f"static/data/club-data.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            if row[5] == club_basic_data[4]:
                club_slogan = row[2]
    starting_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>RHS Clubs</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.form/4.3.0/jquery.form.min.js" integrity="sha384-qlmct0AOBiA2VPZkMY3+2WqkHtIQ9lSdAsAn5RUJD/3vA5MKDgSGcdmIv4ycVxyn" crossorigin="anonymous"></script>
</head>

<body>
<!-- This is all the Navbar stuff: -->
<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">RHS Clubs</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
<a class="nav-link" href="home">Home</a>
                </li>
                <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/explore">Explore</a>
          </li>
                <li class="nav-ite">
<a class="nav-link" href="#">Calendar</a>
                </li>
            </ul>
            <form class="d-flex" role="search">
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
        </div>
    </div>
</nav>
<!-- All the main part of the body -->
<div class="container mt-3 mt-lg-4">
    <div class="row">
        <div class="col-12 col-lg-8">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
<li class="breadcrumb-item"><a href="/" class="text-decoration-none">Home</a></li>
<li class="breadcrumb-item">
    <a href="/explore" class="text-decoration-none">
{club_basic_data[1]}
    </a>
</li>
<li class="breadcrumb-item active" aria-current="page">{club_basic_data[0]}</li>
                </ol>
            </nav>
            <div class="d-flex align-items-center mt-lg-4">
                <img src="{club_basic_data[2]}" class="img-fluid rounded-pill img-thumbnail"
 style="max-width:140px;max-height:140px">
 <div class="container">
    <div class="panel panel-default">
        <div class="panel-heading"><b>Change Icon</b></div>
        <div class="panel-body">
            <form id="uploadImage" method="post" action="/" enctype="multipart/form-data">
                <div class="form-group">
                    <label>File Upload</label>
                    <input type="file" name="uploadFile[]" multiple="false" id="uploadFile" accept=".jpg, .png" />
                </div>
                <div class="form-group">
                    <input type="submit" id="uploadSubmit" value="Upload" class="btn btn-info" />
                </div>
                <div class="progress">
                    <div class="progress-bar progress-bar-striped bg-success" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <div id="targetLayer" style="display:none;"></div>
            </form>
        </div>
    </div>
</div>
                <div class="ms-5">
                    <input class="form-control form-control-lg fw-bold" type="text" placeholder="{club_basic_data[0]}" id="club-name">
                    <input class="form-control form-control-md" type="text" placeholder="{club_slogan}" id="club-slogan" data-toggle="tooltip" data-placement="bottom" title="Club slogan">
                </div>
            </div>
            <div class="container-fluid text-secondary">
                <div class="d-flex justify-content-between align-items-center">
<p class="fw-bold mt-2">Use HTML text formatting!</p>
<a class="btn btn-primary btn-sm rounded-pill" onclick="update_all()">
    Save All <i class="bi bi-save"></i>
</a>
                </div>
                <textarea class="form-control" style="min-width: 100%;min-height:100%;" rows=10 id="description">
"""
    Func.write(starting_code)
    club_desc = Path(f'{real_path}/{club_id}-desc.txt').read_text()
    Func.write(club_desc)
    middle_code = f"""
</textarea>
            </div>
        </div>
        <div class="col-6 col-md-4">
            <div class="card text-center ms-5 shadow">
                <div class="card-header">
Meeting Dates
                </div>
                <div class="card-body">
<input class="fw-bold" placeholder="{club_basic_data[5]}" id="meeting-dates">
                </div>
            </div>
            <div class="card ms-5 mt-5 shadow">
                <div class="card-body">
<h5 class="card-title">Reach out to us!</h5>
<p class="card-text">Check out our socials and contact us if you have any problems!</p>
                </div>
                <ul class="list-group list-group-flush">
"""
    Func.write(middle_code)
    all_data = []
    with open(f'{real_path}/{club_id}-socials.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)

    social_data = all_data[1:]
    for i in range(len(social_data)):
        x = social_data[i]
        socials_code = f"""
    <li class="list-group-item">
    <a onclick="delete_social({i})" href="#"><i class="bi bi-trash"></i></a>
      <span class="ms-2 text-primary">{x[1]}</span>
    </li>
    """
        Func.write(socials_code)
    middle_code_2 = """
<li class="list-group-item">
                        <a onclick="add_social()" href="#"><i class="bi bi-check-square"></i></a>
                        <input class="form-control form-control-md ms-2 text-primary" placeholder="Contact info" id="contact-info">
                        <input class="form-control form-control-md ms-4 text-primary" placeholder="Icon name" id="icon-name">
                    </li>
                </ul>
            </div>
        </div>
    </div>
</div>

<div class="container">
    <h2 class="mt-3">Leadership</h2>
    <div class="row pt-3 px-md-2 px-lg-4 row-cols-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-4 g-3 g-md-5">

"""
    Func.write(middle_code_2)
    all_data = []
    with open(f'{real_path}/{club_id}-leadership.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    leadership_data = all_data[1:]
    for i in range(len(leadership_data)):
        x = leadership_data[i]
        leaders_code = f"""
    <div class="col">
        <div class="card shadow rounded-pill" style="border:0px">
          <div class="d-flex align-items-center ps-2">
            <div style="width:60px;height:60px" class="text-center rounded-pill bg-info">

              <h3 style="margin-top:23%" class="text-white"><a onclick="delete_leadership({i})" href="#"><i class="bi bi-trash"></i></a></h3>

            </div>
            <div>
              <div class="card-body">
                <small class="text-secondary mb-1">{x[1]}</small>
                <h6 class="card-title mb-0">{x[0]}</h6>
              </div>
            </div>
          </div>
        </div>
      </div>
    """
        Func.write(leaders_code)
    ending_code = """
    <div class="col">
            <div class="card shadow rounded-pill" style="border:0px">
                <div class="d-flex align-items-center ps-2">
                    <div style="" class="text-center rounded-pill bg-info">

                        <h3 style="margin-top:23%;marging-right:10px;min-width:100%" class="text-white"><a onclick="add_leadership()" href="#"><i class="bi bi-check-square"></i></a></h3>

                    </div>
                    <div>
                        <div class="card-body">
                            <input class="form-control form-control-md text-secondary" placeholder="Role" id="leader-role">
                            <input class="form-control form-control-md" placeholder="Name" id="leader-name">
                        </div>
                    </div>
                </div>
            </div>
        </div>
<!--        end card-->
    </div>
</div>

<div class="container mt-5">
    <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
        <p class="col-md-4 mb-0 text-muted">Questions? Email <b>aryavratmishra007@gmail.com</b></p>

        <ul class="nav col-md-4 justify-content-end">
            <li class="nav-item"><a href="/" class="nav-link px-2 text-muted">Home</a></li>
            <li class="nav-item"><a href="/explore" class="nav-link px-2 text-muted">Explore</a></li>
            <li class="nav-item"><a href="/calendar" class="nav-link px-2 text-muted">Calendar</a></li>
            <li class="nav-item">
                <p class="nav-link px-2 text-decoration-none opacity-75">Credit: Aryavrat Mishra</p>
            </li>
        </ul>
    </footer>
</div>
<script>
"""
    Func.write(ending_code)
    ending_code1 = f"var clubId = \"{club_id}\";"
    Func.write(ending_code1)
    ending_code2 = """
    $(document).ready(function(){
    $('#uploadImage').submit(function(event){
        if ($('#uploadFile').val()){
            event.preventDefault();

            var formData = new FormData(this);
            formData.append('club_id', clubId);

            $('#loader-icon').show();
            $('#targetLayer').hide();

            $.ajax({
                url: '/upload/'+clubId,  // Replace with the actual URL for your upload endpoint
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                beforeSend: function(){
                    $('.progress-bar').width('50%');
                },
                xhr: function(){
                    var xhr = $.ajaxSettings.xhr();
                    xhr.upload.onprogress = function(event) {
                        if (event.lengthComputable) {
                            var percentageComplete = (event.loaded / event.total) * 100;
                            $('.progress-bar').animate({
                                width: percentageComplete + '%'
                            }, {
                                duration: 1000
                            });
                        }
                    };
                    return xhr;
                },
                success: function(data){
                    $('#loader-icon').hide();
                    $('#targetLayer').show();
                    $('#targetLayer').append(data.htmlresponse);
                }
            });
        }
        return false;
    });
});
    function add_leadership() {
        var leaderRole = $('#leader-role').val();
        var leaderName = $('#leader-name').val();
        console.log({leader_role: leaderRole, leader_name: leaderName, club_id: clubId})
        $.ajax({
            url: '/add_leadership',
            type: 'GET',
            data: {leader_role: leaderRole, leader_name: leaderName, club_id: clubId},
            success: function(response) {
                window.location.reload(true);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
function add_social() {
        var contactInfo = $('#contact-info').val();
        var iconName = $('#icon-name').val();
        $.ajax({
            url: '/add_social',
            type: 'GET',
            data: {contact_info: contactInfo, icon_name: iconName, club_id: clubId},
            success: function(response) {
                location.reload();
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
    function delete_social(socialIndex) {
        $.ajax({
            url: '/delete_social',
            type: 'GET',
            data: {social_index: socialIndex, club_id: clubId},
            success: function(response) {
                location.reload();
            },
            error: function(error) {
                location.reload();
            }
        });
    }
    function delete_leadership(leaderIndex) {
        $.ajax({
            url: '/delete_leadership',
            type: 'GET',
            data: {leader_index: leaderIndex, club_id: clubId},
            success: function(response) {
                location.reload();
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
    function update_all() {
    var description = $('#description').val();
    var name = $('#club-name').val();
    var new_meeting = $('#meeting-dates').val();
    var club_slogan  = $('#club-slogan').val();
    console.log(name)
    var regex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/g    
    var new_club_id = name.replace(regex, '').replace(/[_\s]/g, '-');
        $.ajax({
            url: '/update_all',
            type: 'GET',
            data: {description:description,club_name:name,meeting: new_meeting,club_id: clubId,club_slogan:club_slogan},
            success: function(response) {
            if(name === ""){
                window.location.replace("/view/"+clubId);
            }
            else{
                window.location.replace("/view/"+new_club_id);
            }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
</script>
</body>

</html>
    """
    Func.write(ending_code2)
@app.route('/')  # Route the Function
def main():  # Run the function
    return render_template('home.html')  # Render the template

@app.route('/upload/<club_id>', methods=['POST'])
def upload(club_id):
    if 'uploadFile[]' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('uploadFile[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            # Use club_id as the filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            extension = filename.split(".")[-1]
            try:
                os.remove(f'static/icons/{club_id}.{extension}')
            except:
                pass
            os.rename(f'static/icons/{filename}', f'static/icons/{club_id}.{extension}')
            with open(f"static/data/{club_id}/{club_id}.csv", 'r', newline='') as source, open(f"static/data/{club_id}/{club_id}-results.csv", 'w', newline='') as result:
                csvreader = csv.reader(source)
                csvwriter = csv.writer(result)
                header = next(csvreader)
                csvwriter.writerow(header)
                for row in csvreader:
                    row[2] = f'/static/icons/{club_id}.{extension}'
                    csvwriter.writerow(row)
            os.remove(f"static/data/{club_id}/{club_id}.csv")
            os.rename(f"static/data/{club_id}/{club_id}-results.csv",f"static/data/{club_id}/{club_id}.csv")
            with open(f"static/data/club-data.csv", 'r', newline='') as source, open(f"static/data/club-data-results.csv", 'w', newline='') as result:
                csvreader = csv.reader(source)
                csvwriter = csv.writer(result)
                header = next(csvreader)
                csvwriter.writerow(header)
                for row in csvreader:
                    if row[5] == club_id:
                        row[1] = f'/static/icons/{club_id}.{extension}'
                    csvwriter.writerow(row)
            os.remove(f"static/data/club-data.csv")
            os.rename(f"static/data/club-data-results.csv",f"static/data/club-data.csv")
            file_names.append(f"{club_id}.{extension}")
            msg = 'File successfully uploaded!'
        else:
            msg = 'Failed to upload, please try again!'
    return jsonify({'htmlresponse': render_template('response.html', msg=msg, filenames=file_names)})

@app.route('/home')  # Route the Function
def home():  # Run the function
    return render_template('home.html')  # Render the template


@app.route('/explore')  # Route the Function
def explore():  # Run the function
    quick_create_explore()
    return render_template('explore.html')  # Render the template


@app.route('/view/<club_id>')  # /landingpage/A
def view_page(club_id):
    real_path = f"static/data/{club_id}"
    all_data = []
    with open(f"{real_path}/{club_id}.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    club_basic_data = all_data[1]
    print(club_basic_data)
    category = club_basic_data[1]
    club_name = club_basic_data[0]
    club_id = club_basic_data[4]
    meeting_date = club_basic_data[5]
    filename = club_basic_data[2]
    time_update = club_basic_data[3]
    desc = Path(f'{real_path}/{club_id}-desc.txt').read_text()
    all_data = []
    with open(f'{real_path}/{club_id}-socials.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    socials_list = all_data[1:]
    all_data = []
    with open(f'{real_path}/{club_id}-leadership.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    leaders_list = all_data[1:]
    return render_template('club-view.html', club_id=club_id,time_update = time_update, category=category, club_name=club_name,meeting_date=meeting_date,filename=filename,desc=desc,socials_list=socials_list,leaders_list=leaders_list)

@app.route('/verify_credentials')
def verification():
    username = request.args.get('username')
    password = request.args.get('password')
    club_id = request.args.get('club_id')
    with open(f"static/data/{club_id}/{club_id}.csv", 'r', newline='') as source:
        csvreader = csv.reader(source)
        header = next(csvreader)
        for row in csvreader:
            real_username = row[6]
            real_password = row[7]
    if (real_username == username and real_password == password) or (username == "admin" and password=="admin"):
        return {"valid": "True"}
    else:
        return {"valid": "False"}
@app.route('/edit/<club_id>')  # /landingpage/A
def editing_page(club_id):
    username = request.args.get('username')
    password = request.args.get('password')
    with open(f"static/data/{club_id}/{club_id}.csv", 'r', newline='') as source:
        csvreader = csv.reader(source)
        header = next(csvreader)
        for row in csvreader:
            real_username = row[6]
            real_password = row[7]
    if (real_username == username and real_password == password) or (username == "admin" and password=="admin"):
        real_path = f"static/data/{club_id}"
        all_data = []
        with open(f"{real_path}/{club_id}.csv", 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            for row in csvreader:
                all_data.append(row)
        club_basic_data = all_data[1]
        category = club_basic_data[1]
        club_name = club_basic_data[0]
        meeting_date = club_basic_data[5]
        filename = club_basic_data[2]
        desc = Path(f'{real_path}/{club_id}-desc.txt').read_text()
        all_data = []
        with open(f'{real_path}/{club_id}-socials.csv') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=',')
            for row in csvreader:
                all_data.append(row)
        socials_list = all_data[1:]
        all_data = []
        with open(f'{real_path}/{club_id}-leadership.csv') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=',')
            for row in csvreader:
                all_data.append(row)
        leaders_list = all_data[1:]
        club_slogan = ""
        with open(f"static/data/club-data.csv", 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            for row in csvreader:
                if row[5] == club_basic_data[4]:
                    club_slogan = row[2]
        return render_template('club-edit.html', socials_len = len(socials_list), leaders_len = len(leaders_list), club_slogan=club_slogan, category=category, club_id=club_id, club_name=club_name,meeting_date=meeting_date,filename=filename,desc=desc,socials_list=socials_list,leaders_list=leaders_list)
    else:
        return render_template('unauth-access.html', club=club_id)

@app.route('/login/<club_id>')
def login_page(club_id):
    return render_template(f'club-login.html',club_id=club_id)


def update_time(club_id):
    with open(f"static/data/{club_id}/{club_id}.csv", 'r', newline='') as source, open(f"static/data/{club_id}/{club_id}-results.csv", 'w', newline='') as result:
        csvreader = csv.reader(source)
        csvwriter = csv.writer(result)
        header = next(csvreader)
        csvwriter.writerow(header)
        for row in csvreader:
            row[3] = str(datetime.now(timezone.utc)).replace(" ","T").split(".")[0]
            csvwriter.writerow(row)
    os.remove(f"static/data/{club_id}/{club_id}.csv")
    os.rename(f"static/data/{club_id}/{club_id}-results.csv", f"static/data/{club_id}/{club_id}.csv")
    with open(f"static/data/club-data.csv", 'r', newline='') as source, open(f"static/data/club-data-results.csv", 'w', newline='') as result:
        csvreader = csv.reader(source)
        csvwriter = csv.writer(result)
        header = next(csvreader)
        csvwriter.writerow(header)
        for row in csvreader:
            if row[5] == club_id:
                row[4] = str(datetime.now(timezone.utc)).replace(" ","T").split(".")[0]
            csvwriter.writerow(row)
    os.remove(f"static/data/club-data.csv")
    os.rename(f"static/data/club-data-results.csv", f"static/data/club-data.csv")

@app.route('/add_leadership')
def add_leadership():
    leader_role = request.args.get('leader_role')
    leader_name = request.args.get('leader_name')
    club_id = request.args.get('club_id')
    update_time(club_id)
    with open(f"static/data/{club_id}/{club_id}-leadership.csv",
              'a',
              newline='',
              encoding='utf-8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow([
            leader_name, leader_role,
            ''.join([x[0].upper() for x in leader_name.split(' ')])
        ])
    return jsonify(result="Success!")


@app.route('/add_social')
def add_social():
    contact_info = request.args.get('contact_info')
    icon_name = request.args.get('icon_name')
    club_id = request.args.get('club_id')
    update_time(club_id)
    with open(f"static/data/{club_id}/{club_id}-socials.csv",
              'a',
              newline='',
              encoding='utf-8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow([icon_name, contact_info])
    return jsonify(result="Success!")


@app.route('/delete_social')
def delete_social():
    row_number = request.args.get('social_index')
    club_id = request.args.get('club_id')
    update_time(club_id)
    csv_file = f"static/data/{club_id}/{club_id}-socials.csv"
    delete_real_row(csv_file, int(row_number))


@app.route('/delete_leadership')
def delete_leadership():
    leader_index = request.args.get('leader_index')
    club_id = request.args.get('club_id')
    update_time(club_id)
    delete_real_row(f"static/data/{club_id}/{club_id}-leadership.csv",
                    int(leader_index))
    return jsonify(result="Success!")


@app.route('/update_all')
def update_all():
    description = request.args.get('description')
    name = request.args.get('club_name')
    meeting = request.args.get('meeting')
    club_id = request.args.get('club_id')
    club_slogan = request.args.get('club_slogan')
    update_time(club_id)
    with open(f"static/data/{club_id}/{club_id}-desc.txt", "w") as text_file:
        text_file.write(description)
    trim_newlines(f"static/data/{club_id}/{club_id}-desc.txt")
    if meeting != "":
        with open(f"static/data/{club_id}/{club_id}.csv", 'r', newline='') as source, open(f"static/data/{club_id}/{club_id}-results.csv", 'w', newline='') as result:
            csvreader = csv.reader(source)
            csvwriter = csv.writer(result)
            header = next(csvreader)
            csvwriter.writerow(header)
            for row in csvreader:
                row[5] = meeting
                csvwriter.writerow(row)
        os.remove(f"static/data/{club_id}/{club_id}.csv")
        os.rename(f"static/data/{club_id}/{club_id}-results.csv", f"static/data/{club_id}/{club_id}.csv")
    if club_slogan != "":
        with open(f"static/data/club-data.csv", 'r', newline='') as source, open(f"static/data/club-data-results.csv", 'w', newline='') as result:
            csvreader = csv.reader(source)
            csvwriter = csv.writer(result)
            header = next(csvreader)
            csvwriter.writerow(header)
            for row in csvreader:
                if row[5] == club_id:
                    row[2] = club_slogan
                csvwriter.writerow(row)
        os.remove("static/data/club-data.csv")
        os.rename("static/data/club-data-results.csv", "static/data/club-data.csv")
    if name != "":
        new_club_id = re.sub(r'[^a-zA-Z0-9\s]', '', name)
        new_club_id = new_club_id.replace(' ', '-')
        if new_club_id == club_id:
            return jsonify(result="Success!")
        os.mkdir(f"static/data/{new_club_id}")
        with open(f"static/data/{club_id}/{club_id}.csv", 'r', newline='') as source, open(f"static/data/{new_club_id}/{new_club_id}.csv", 'w', newline='') as result:
            csvreader = csv.reader(source)
            csvwriter = csv.writer(result)
            header = next(csvreader)
            csvwriter.writerow(header)
            for row in csvreader:
                row[0] = name
                row[4] = new_club_id
                csvwriter.writerow(row)
        os.rename(f"static/data/{club_id}/{club_id}-leadership.csv",f"static/data/{new_club_id}/{new_club_id}-leadership.csv")
        os.rename(f"static/data/{club_id}/{club_id}-socials.csv", f"static/data/{new_club_id}/{new_club_id}-socials.csv")
        os.rename(f"static/data/{club_id}/{club_id}-desc.txt", f"static/data/{new_club_id}/{new_club_id}-desc.txt")
        try:
            shutil.rmtree(f"static/data/{club_id}")
        except OSError as e:
            print(e)
        with open(f"static/data/club-data.csv", 'r', newline='') as source, open(f"static/data/club-data-results.csv", 'w', newline='') as result:
            csvreader = csv.reader(source)
            csvwriter = csv.writer(result)
            header = next(csvreader)
            csvwriter.writerow(header)
            for row in csvreader:
                if row[5] == club_id:
                    row[5] = new_club_id
                    row[0] = name
                csvwriter.writerow(row)
    return jsonify(result="Success!")

@app.route('/test')
def test():
    club_id = "Bird-Club"
    real_path = f"static/data/{club_id}"
    all_data = []
    with open(f"{real_path}/{club_id}.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    club_basic_data = all_data[1]
    print(club_basic_data)
    category = club_basic_data[1]
    club_name = club_basic_data[0]
    meeting_date = club_basic_data[5]
    filename = club_basic_data[2]
    desc = Path(f'{real_path}/{club_id}-desc.txt').read_text()
    all_data = []
    with open(f'{real_path}/{club_id}-socials.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    socials_list = all_data[1:]
    all_data = []
    with open(f'{real_path}/{club_id}-leadership.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    leaders_list = all_data[1:]
    print(leaders_list)
    return render_template('club-view.html', category=category, club_name=club_name,meeting_date=meeting_date,filename=filename,desc=desc,socials_list=socials_list,leaders_list=leaders_list)


app.run(host='0.0.0.0', port=5000,debug=True)