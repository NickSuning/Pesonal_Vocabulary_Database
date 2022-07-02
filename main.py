from website import create_app

app = create_app()

if __name__ == '__main__':  #only running main instead of importing from website
    app.run(debug=True) #debug mode: new change will trigger re-running of codes. Off in production file


