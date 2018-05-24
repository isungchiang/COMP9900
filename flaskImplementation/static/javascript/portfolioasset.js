var myChart = echarts.init(document.getElementById("portlolioasset"));
var stockNamelist = []
var stockGainlist = []
var portfoliosInfo = {}
var labelRight = {
    normal: {
        position: 'right'
    }
};
var labelLeft = {
    normal: {
        position: 'left'
    }
};


var portfolioname = '{{ portfolio }}';
var portfolio = window.portfolios[portfolioname];
if (portfolio.length > 0) {
    var stocks = {}
    for (var stock in portfolio){
        var stockid = portfolio[stock]['StockId']
        if (stockid in stocks){
            stocks[stockid]['Shares'] += parseInt(portfolio[stock]['Shares'])
            stocks[stockid]['Original Asset'] += parseFloat(portfolio[stock]['Shares'])*parseFloat(portfolio[stock]['TradePrice'])
        }
        else{
            stocks[stockid] = {}
            stocks[stockid]['Shares'] = parseInt(portfolio[stock]['Shares'])
            stocks[stockid]['Original Asset'] = parseFloat(portfolio[stock]['Shares'])*parseFloat(portfolio[stock]['TradePrice'])
             $.ajax({
                async: false,
                url: 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stockid+'&apikey=FXO9ZICGVO904HHE',
                success: function (stock_data) {
                    var lastdate = stock_data['Meta Data']['3. Last Refreshed']
                    stocks[stockid]['Latest Price'] = parseFloat(stock_data['Time Series (Daily)'][lastdate]['4. close'])
                    stocks[stockid]['Latest Change'] = (parseFloat(stock_data['Time Series (Daily)'][lastdate]['4. close']) - parseFloat(stock_data['Time Series (Daily)'][lastdate]['1. open'])) / parseFloat(stock_data['Time Series (Daily)'][lastdate]['1. open']) * 100
                }
            })
        }
    }
    var totalGain = 0
    var totalAsset = 0
    var totalOriginalAsset = 0
    for (var stockid in stocks){
        stocks[stockid]['Current Asset'] = stocks[stockid]['Shares'] * stocks[stockid]['Latest Price']
        stocks[stockid]['Total Gain'] = stocks[stockid]['Current Asset'] - stocks[stockid]['Original Asset']
        stocks[stockid]['Total Gain Percentage'] = stocks[stockid]['Total Gain'] / stocks[stockid]['Original Asset'] * 100
        totalGain += stocks[stockid]['Total Gain']
        totalAsset += stocks[stockid]['Current Asset']
        totalOriginalAsset += stocks[stockid]['Original Asset']
        stockNamelist.push(portfolioname+':'+stockid)
        if (stocks[stockid]['Total Gain']>=0){
            stockGainlist.push({value:stocks[stockid]['Total Gain'],label:labelRight})
        }else{
            stockGainlist.push({value:stocks[stockid]['Total Gain'],label:labelLeft})
        }

    }
    var portfolioInfo = {}
    portfolioInfo['Stock Info'] = stocks
    portfolioInfo['Portfolio Info'] = {'Total Asset':totalAsset, 'Total Original Asset':totalOriginalAsset, 'Total Gain':totalGain}

    portfoliosInfo[portfolioname] = portfolioInfo
}
else{
    document.write('<h2>This portfolio is currently empty</h2>');
}

console.log(portfolioInfo)

option = {
    title: {
        text: 'Gain Table',
        subtext: 'From ExcelHome',
        sublink: 'http://e.weibo.com/1341556070/AjwF2AgQm'
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {
            type : 'shadow'
        }
    },
    grid: {
        top: 80,
        bottom: 30
    },
    xAxis: {
        type : 'value',
        position: 'top',
        splitLine: {lineStyle:{type:'dashed'}},
    },
    yAxis: {
        type : 'category',
        axisLine: {show: false},
        axisLabel: {show: false},
        axisTick: {show: false},
        splitLine: {show: false},
        data : stockNamelist,
    },
    series : [
        {
            name:'Gain',
            type:'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    formatter: '{b}'
                }
            },
            data:stockGainlist,
        }
    ]
};

myChart.setOption(option);