from flask import Flask, render_template, jsonify, request  # Import Flask Class, and render_template
import pandas as pd
import csv
from pathlib import Path

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)

app = Flask(__name__)  # Create an Instance


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
  <link href="static/css/style.css" rel="stylesheet" type="text/css" />
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
  <script src="static/scripts/explore-script.js"></script>
</body>

</html>
"""
    Func.write(closing_code)
    Func.close()


def view_website(club_id):
    real_path = f"static/data/{club_id}"
    Func = open(f"templates/{club_id}-view.html", "w")
    all_data = []
    with open(f"{real_path}/{club_id}.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    club_basic_data = all_data[1:][0]
    starting_code = f"""
  <!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="30">
  <meta name="viewport" content="width=device-width">
  <title>RHS Clubs</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
  <link href="static/css/style.css" rel="stylesheet" type="text/css" />
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
            <div class="ms-5">
              <h1 class="fw-bold">{club_basic_data[0]}</h1>
            </div>
          </div>
          <div class="container-fluid text-secondary">
            <div class="d-flex justify-content-between align-items-center">
              <p class="fw-bold mt-2">Last modified: 3 months ago</p>
              <a class="btn btn-primary btn-sm rounded-pill" href="/edit/{club_basic_data[4]}">
                Edit <i class="bi bi-pen"></i>
              </a>
            </div>
  """
    Func.write(starting_code)
    club_desc = Path(f'{real_path}/{club_id}-desc.txt').read_text()
    Func.write(club_desc)
    middle_code = f"""
  </div>
  </div>
  <div class="col-6 col-md-4">
    <div class="card text-center ms-5 shadow">
      <div class="card-header">
        Meeting Dates
      </div>
      <div class="card-body">
        <h5 class="card-title">{club_basic_data[5]}</h5>
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
    for i in social_data:
        socials_code = f"""
    <li class="list-group-item">
    <i class="bi {i[0]}"></i>
      <span class="ms-2 text-primary">{i[1]}</span>
    </li>
    """
        Func.write(socials_code)
    second_middle_code = """
  </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="container">
    <h2 class="mt-3">Leadership</h2>
    <div class="row pt-3 px-md-2 px-lg-4 row-cols-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-4 g-3 g-md-5">
    """
    Func.write(second_middle_code)
    all_data = []
    with open(f'{real_path}/{club_id}-leadership.csv') as csv_file:
        csvreader = csv.reader(csv_file, delimiter=',')
        for row in csvreader:
            all_data.append(row)
    leadership_data = all_data[1:]
    for i in leadership_data:
        socials_code = f"""
    <div class="col">
        <div class="card shadow rounded-pill" style="border:0px">
          <div class="d-flex align-items-center ps-2">
            <div style="width:60px;height:60px" class="text-center rounded-pill bg-info">

              <h3 style="margin-top:23%" class="text-white">{i[2]}</h3>

            </div>
            <div>
              <div class="card-body">
                <small class="text-secondary mb-1">{i[1]}</small>
                <h6 class="card-title mb-0">{i[0]}</h6>
              </div>
            </div>
          </div>
        </div>
      </div>
    """
        Func.write(socials_code)
    ending_code = """
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
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"
      integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <script src="explore-script.js"></script>
  </body>

  </html>
  """
    Func.write(ending_code)
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
    starting_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="30">
    <meta name="viewport" content="width=device-width">
    <title>RHS Clubs</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
    <link href="static/css/style.css" rel="stylesheet" type="text/css" />
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
                <div class="ms-5">
                    <input class="form-control form-control-lg fw-bold" type="text" placeholder="{club_basic_data[0]}" id="club-name">
                </div>
            </div>
            <div class="container-fluid text-secondary">
                <div class="d-flex justify-content-between align-items-center">
<p class="fw-bold mt-2">Use HTML text formatting!</p>
<a class="btn btn-primary btn-sm rounded-pill" href="/edit/Bird-Club">
    Save All <i class="bi bi-save"></i>
</a>
                </div>
                <textarea class="form-control" style="min-width: 100%;min-height:100%;" rows=10 id="desc">
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
<input class="card-title fw-bold" placeholder="{club_basic_data[5]}">
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
    middle_code_2 = f"""
<li class="list-group-item">
                        <a onclick="add_social()" href="#"><i class="bi bi-check-square"></i></a>
                        <input class="ms-2 text-primary" placeholder="Contact info">
                        <input class="ms-4 text-primary" placeholder="Social name">
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
                            <input class="text-secondary" placeholder="Role" id="leader-role">
                            <input class="" placeholder="Name" id="leader-name">
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
<script src="https://code.jquery.com/jquery-3.5.1.min.js"
        integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
<script src="explore-script.js"></script>
<script>
    var clubId = "Bird-Club";
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

</script>
</body>

</html>
    """
    Func.write(ending_code)
@app.route('/')  # Route the Function
def main():  # Run the function
    return render_template('home.html')  # Render the template


@app.route('/home')  # Route the Function
def home():  # Run the function
    return render_template('home.html')  # Render the template


@app.route('/explore')  # Route the Function
def explore():  # Run the function
    quick_create_explore()
    return render_template('explore.html')  # Render the template


@app.route('/view/<club>')  # /landingpage/A
def landing_page(club):
    view_website(club)
    return render_template(f'{club}-view.html', club=club)

@app.route('/edit/<club>')  # /landingpage/A
def editing_page(club):
    edit_website(club)
    return render_template(f'{club}-edit.html', club=club)

@app.route('/add_leadership')
def call_python_function():
    leader_role = request.args.get('leader_role')
    leader_name = request.args.get('leader_name')
    club_id = request.args.get('club_id')
    print(leader_role,leader_name)
    with open(f"static/data/{club_id}/{club_id}-leadership.csv", 'a',newline='', encoding='utf-8') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow([leader_name, leader_role, ''.join([x[0].upper() for x in leader_name.split(' ')])])
    return jsonify(result="Success!")

app.run(host='0.0.0.0', port=5000,
        debug=True)  # Run the Application (in debug mode)
