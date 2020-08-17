from flask import Flask, render_template, request
from app import application, create_plot


app = Flask(__name__)



@app.route('/api/info', methods  = ['GET'])
def info():
    '''
    This method gives you an information about the data.
    :return: web-page with info
    '''
    bar = create_plot()
    return render_template('index.html', plot=bar)



@app.route('/api/timeline', methods  = ['GET'])
def timeline():
    '''
    This method does the data visualization.
    Test link: '/api/timeline?startDate=11/26/2018+22:00:00&endDate=11/20/2019+22:00:00&stars=5&source=amazon&type=usual&grouping=weekly'
    :return: web-page with data visualization
    '''
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    stars = request.args.get('stars')
    asin = request.args.get('asin')
    brand = request.args.get('brand')
    source = request.args.get('source')
    type = request.args.get('type')
    grouping = request.args.get('grouping')
    bar = application(startDate, endDate, stars, asin, brand, source, type, grouping)
    return render_template('plot.html', plot=bar)

if __name__ == '__main__':
    app.run()
