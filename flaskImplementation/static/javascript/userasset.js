var myChart = echarts.init(document.getElementById('userassets'));
var stockNamelist = []
var stockGainlist = []
var portfoliosInfo = {}
var count = false
var labelRight = {
    normal: {
        position: 'right',
    }
};
var labelLeft = {
    normal: {
        position: 'left'
    }
};
var itemRight={
    normal:{
        color:'#69d694'
    }
};
for (portfolioname in window.portfolios) {
    var portfolio = window.portfolios[portfolioname]
    if (portfolio.length > 0) {
        count = true
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
                stockGainlist.push({value:stocks[stockid]['Total Gain'],label:labelRight,itemStyle:itemRight})
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
        continue
    }
}
// console.log(portfoliosInfo)
if (count == false){
    document.write('<h2>This portfolio is currently empty</h2>');
}
// if (portfolioInfo['Portfolio Info']['Total Asset']==0){
//     document.write('<h2>This portfolio is currently empty</h2>');
// }

option = {
    title: {
        text: 'Gain Table'
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
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