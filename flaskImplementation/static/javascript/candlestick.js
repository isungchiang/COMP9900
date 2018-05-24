 var myChart = echarts.init(document.getElementById('main'));
 var data0;
 var data1;
 var data2;
 var stockid = $("#StockID").data("result");
var downColor = '#ec0000';
var downBorderColor = '#8A0000';
var upColor = '#00da3c';
var upBorderColor = '#008F28';

 $.ajax({
    async: false,
    url: 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stockid+'&apikey=FXO9ZICGVO904HHE',
    success: function (stock_data) {
        data0 = newSplit(stock_data['Time Series (Daily)'])
    }
 });

  $.ajax({
    async: false,
    url: 'https://www.alphavantage.co/query?function=RSI&symbol='+stockid+'&interval=daily&time_period=15&series_type=open&apikey=FXO9ZICGVO904HHE',
    success: function (stock_data) {
        data1 = rsi(stock_data['Technical Analysis: RSI'], data0)
    }
 });

  $.ajax({
    async: false,
    url: 'https://www.alphavantage.co/query?function=WILLR&symbol='+stockid+'&interval=daily&time_period=21&series_type=open&apikey=FXO9ZICGVO904HHE',
    success: function (stock_data) {
        data2 = willr(stock_data['Technical Analysis: WILLR'], data0)
    }
 });

 function newSplit(data) {
     var categoryData = [];
     var values = [];

     for (var timeseries in data) {
         categoryData.push(timeseries);
         var value = [];
         value.push(parseFloat(data[timeseries]['1. open']));
         value.push(parseFloat(data[timeseries]['4. close']));
         value.push(parseFloat(data[timeseries]['3. low']));
         value.push(parseFloat(data[timeseries]['2. high']));
         values.push(value.splice(0, 4));

     }
     return {
             categoryData: categoryData.reverse(),
             values: values.reverse()
     };
 }

  function rsi(data, data_1) {
     var categoryData = [];
     var values = [];

     for (var timeseries=0, len=data_1.categoryData.length;timeseries<len-1;timeseries++){
         categoryData.push(data_1.categoryData[timeseries]);
         values.push(parseFloat((data[data_1.categoryData[timeseries]])['RSI']));
     }
     return {
             categoryData: categoryData.reverse(),
             values: values.reverse()
     };
 }

   function willr(data, data_1) {
     var categoryData = [];
     var values = [];

     for (var timeseries=0, len=data_1.categoryData.length;timeseries<len-1;timeseries++){
         categoryData.push(data_1.categoryData[timeseries]);
         values.push(Math.abs(parseFloat((data[data_1.categoryData[timeseries]])['WILLR'])));
     }
     return {
             categoryData: categoryData.reverse(),
             values: values.reverse()
     };
 }

 // data_1: timeseries, data_2: rsi
 function analyzersi(data_1, data_2) {
     var buy = [];
     var sell = [];

     for(var i=0, len=data_2.length;i<len;i++) {
         if(i > 1) {
             if(data_2[i] >
                 data_2[i-1] &&
                 data_2[i-1]  >
                 data_2[i-2] &&
                 data_2[i] <= 70 &&
                 data_2[i-2] >=40) {
                 buy.push((data_1.values[i])[2]-5);
             }
             else if(data_2[i]<=10.0) {
                 buy.push((data_1.values[i])[2]-5);
             }
             else {
                 buy.push(null);
             }

         }
         else {
             buy.push(null);
         }

         if(i > 1) {
             if(data_2[i] <
                 data_2[i-1] &&
                 data_2[i-1]  <
                 data_2[i-2] &&
                 data_2[i] >=50) {
                 sell.push((data_1.values[i])[3]+5);
             }
             else if(data_2[i]>=85.0) {
                 sell.push((data_1.values[i])[3]+5);
             }
             else {
                 sell.push(null);
             }
         }
         else {
             sell.push(null);
         }
     }

     return {
         sells: sell,
         buys  : buy
     };


 }

 function analyzewiir(data_1, data_2) {
     var buy = [];
     var sell = [];

     for(var i=0, len=data_2.length;i<len;i++) {
         if(i>1) {
            if(data_2[i] >= 85) {
                sell.push((data_1.values[i])[3]+8);
            }
            else {
                sell.push(null);
            }

            if(data_2[i] <=10) {
                buy.push((data_1.values[i])[2]-8);
            }
            else {
                buy.push(null);
            }
         }
         else {
             buy.push(null);
             sell.push(null);
         }
     }
     // console.log(buy);
     return {
         sells: sell,
         buys: buy
     }
 }

function calculateMA(dayCount) {
    var result = [];
    for (var i = 0, len = data0.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data0.values[i - j][1];
        }

        result.push(sum / dayCount);
    }
    return result;
}



option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        }
    },
    legend: {
        data: ['Daily', 'MA5', 'MA10', 'MA20', 'MA30',
            'RSI_Buy', 'RSI_Sell', 'WILLR_Buy', 'WILLR_Sell']
    },
    grid: {
        left: '10%',
        right: '10%',
        bottom: '15%'
    },
    xAxis: {
        type: 'category',
        data: data0.categoryData,
        scale: true,
        boundaryGap : false,
        axisLine: {onZero: false},
        splitLine: {show: false},
        splitNumber: 20,
        min: 'dataMin',
        max: 'dataMax'
    },
    yAxis: {
        scale: true,
        splitArea: {
            show: true
        }
    },
    dataZoom: [
        {
            type: 'inside',
            start: 50,
            end: 100
        },
        {
            show: true,
            type: 'slider',
            y: '90%',
            start: 50,
            end: 100
        }
    ],
    series: [
        {
            name: 'Daily',
            type: 'candlestick',
            data: data0.values,
            itemStyle: {
                normal: {
                    color: upColor,
                    color0: downColor,
                    borderColor: upBorderColor,
                    borderColor0: downBorderColor
                }
            },
            markPoint: {
                label: {
                    normal: {
                        formatter: function (param) {
                            return param != null ? Math.round(param.value) : '';
                        }
                    }
                },
                data: [
                    {
                        name: 'XX标点',
                        coord: ['2013/5/31', 2300],
                        value: 2300,
                        itemStyle: {
                            normal: {color: 'rgb(41,60,85)'}
                        }
                    },
                    {
                        name: 'highest value',
                        type: 'max',
                        valueDim: 'highest',
                        itemStyle: {
                            normal: {color: upBorderColor}
                        }
                    },
                    {
                        name: 'lowest value',
                        type: 'min',
                        valueDim: 'lowest',
                        itemStyle: {
                            normal: {color: downBorderColor}
                        }
                    },
                    {
                        name: 'average value on close',
                        type: 'average',
                        valueDim: 'close'
                    }
                ],
                tooltip: {
                    formatter: function (param) {
                        return param.name + '<br>' + (param.data.coord || '');
                    }
                }
            },
        },
        {
            name: 'MA5',
            type: 'line',
            data: calculateMA(5),
            smooth: true,
            lineStyle: {
                normal: {opacity: 0.5}
            }
        },
        {
            name: 'MA10',
            type: 'line',
            data: calculateMA(10),
            smooth: true,
            lineStyle: {
                normal: {opacity: 0.5}
            }
        },
        {
            name: 'MA20',
            type: 'line',
            data: calculateMA(20),
            smooth: true,
            lineStyle: {
                normal: {opacity: 0.5}
            }
        },
        {
            name: 'MA30',
            type: 'line',
            data: calculateMA(30),
            smooth: true,
            lineStyle: {
                normal: {opacity: 0.5}
            }
        },

        {
            name: 'RSI_Buy',
            type: 'scatter',
            data: (analyzersi(data0, data1.values)).buys,
            symbol: 'triangle',
            color: downColor
        },

        {
            name: 'RSI_Sell',
            type: 'scatter',
            data: (analyzersi(data0, data1.values)).sells,
            symbol: 'diamond',
            color: upColor
        },

        {
            name: 'WILLR_Buy',
            type: 'scatter',
            data: (analyzewiir(data0, data2.values)).buys,
            symbol: 'emptyTriangle',
            color: downColor
        },

        {
            name: 'WILLR_Sell',
            type: 'scatter',
            data: (analyzewiir(data0, data2.values)).sells,
            symbol: 'emptyDiamond',
            color: upColor
        },




    ]
};

 myChart.setOption(option);