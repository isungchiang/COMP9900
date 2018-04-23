 var myChart = echarts.init(document.getElementById('main'));
 var data0;
 var data1;
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
    url: 'https://www.alphavantage.co/query?function=RSI&symbol='+stockid+'&interval=daily&time_period=7&series_type=open&apikey=FXO9ZICGVO904HHE',
    success: function (stock_data) {
        data1 = rsi(stock_data['Technical Analysis: RSI'])
    }
 });

 function newSplit(data) {
     var categoryData = [];
     var values = [];

     for (var timeseries in data){
         categoryData.push(timeseries);
         var value = [];
         // for (var item in data[timeseries]){
         //     value.push(parseFloat(data[timeseries][item]));
         // }
         value.push(parseFloat(data[timeseries]['1. open']));
         value.push(parseFloat(data[timeseries]['4. close']));
         value.push(parseFloat(data[timeseries]['3. low']));
         value.push(parseFloat(data[timeseries]['2. high']));
         values.push(value.splice(0,4));
     }
     return {
             categoryData: categoryData.reverse(), //数组中的日期 x轴对应的日期
             values: values.reverse()  //数组中的数据 y轴对应的数据
     };
 }

  function rsi(data) {
     var categoryData = [];
     var values = [];

     for (var timeseries in data){
         categoryData.push(timeseries);
         values.push(parseFloat(data[timeseries]['RSI']));
     }
     return {
             categoryData: categoryData.reverse(), //数组中的日期 x轴对应的日期
             values: values.reverse()  //数组中的数据 y轴对应的数据
     };
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
    title: {
        text: stockid,
        left: 0
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        }
    },
    legend: {
        data: ['Daily', 'MA5', 'MA10', 'MA20', 'MA30', 'RSI']
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
            markLine: {
                symbol: ['none', 'none'],
                data: [
                    [
                        {
                            name: 'from lowest to highest',
                            type: 'min',
                            valueDim: 'lowest',
                            symbol: 'circle',
                            symbolSize: 10,
                            label: {
                                normal: {show: false},
                                emphasis: {show: false}
                            }
                        },
                        {
                            type: 'max',
                            valueDim: 'highest',
                            symbol: 'circle',
                            symbolSize: 10,
                            label: {
                                normal: {show: false},
                                emphasis: {show: false}
                            }
                        }
                    ],
                    {
                        name: 'min line on close',
                        type: 'min',
                        valueDim: 'close'
                    },
                    {
                        name: 'max line on close',
                        type: 'max',
                        valueDim: 'close'
                    }
                ]
            }
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
            name: 'RSI',
            type: 'scatter',
            data: data1.values,
            symbol: 'triangle'
        },


    ]
};


 // 使用刚指定的配置项和数据显示图表
 myChart.setOption(option);