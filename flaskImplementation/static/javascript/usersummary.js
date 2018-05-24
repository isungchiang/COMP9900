var myChart = echarts.init(document.getElementById('usersummary'));
var portfoliosInfo = {}
var portfoliosNamelist = []
var portfoliosDatalist = []
var stocksDatalist = []
var count = false
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
            stocksDatalist.push({value:stocks[stockid]['Current Asset'],name:portfolioname+':'+stockid})
        }
        var portfolioInfo = {}
        portfolioInfo['Stock Info'] = stocks
        portfolioInfo['Portfolio Info'] = {'Total Asset':totalAsset, 'Total Original Asset':totalOriginalAsset, 'Total Gain':totalGain}
        portfoliosInfo[portfolioname] = portfolioInfo

        portfoliosDatalist.push({value:totalAsset,name:portfolioname})
        portfoliosNamelist.push(portfolioname)
    }
    else{
        continue
    }
}
// console.log(count)
if (count == false){
    document.write('<h2>This portfolio is currently empty</h2>');
}
option = {
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data:[],
    },
    series: [
        {
            name:'Current Asset',
            type:'pie',
            selectedMode: 'single',
            radius: [0, '30%'],

            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data:stocksDatalist,
        },
        {
            name:'Total Asset',
            type:'pie',
            radius: ['40%', '55%'],
            label: {
                normal: {
                    formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                    backgroundColor: '#eee',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    borderRadius: 4,
                    // shadowBlur:3,
                    // shadowOffsetX: 2,
                    // shadowOffsetY: 2,
                    // shadowColor: '#999',
                    // padding: [0, 7],
                    rich: {
                        a: {
                            color: '#999',
                            lineHeight: 22,
                            align: 'center'
                        },
                        // abg: {
                        //     backgroundColor: '#333',
                        //     width: '100%',
                        //     align: 'right',
                        //     height: 22,
                        //     borderRadius: [4, 4, 0, 0]
                        // },
                        hr: {
                            borderColor: '#aaa',
                            width: '100%',
                            borderWidth: 0.5,
                            height: 0
                        },
                        b: {
                            fontSize: 16,
                            lineHeight: 33
                        },
                        per: {
                            color: '#eee',
                            backgroundColor: '#334455',
                            padding: [2, 4],
                            borderRadius: 2
                        }
                    }
                }
            },
            data:portfoliosDatalist,
        }
    ]
};

myChart.setOption(option);
