# pulling in the function from __init__
from Website import create_app

app = create_app()

# when you run the file it runs the web server
if __name__ == '__main__':
    # run flask app and rerun for each change (turn off in prod)
    app.run(debug=True)