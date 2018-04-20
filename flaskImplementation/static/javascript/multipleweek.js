 var myChart = echarts.init(document.getElementById('weekly'));
 var data0;
 var stockid = $("#StockID").data("result");
 $.ajax({
    async: false,
    url: 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+stockid+'&apikey=FXO9ZICGVO904HHE',
    success: function (stock_data) {
            data0 = newSplit(stock_data['Weekly Time Series']);
    }
 });

 function newSplit(data) {
     var categoryData = [];
     var price = [];
     var volume = [];

     for (var timeseries in data){
         categoryData.push(timeseries);
         price.push((parseFloat(data[timeseries]["1. open"])+parseFloat(data[timeseries]["4. close"]))/2);
         volume.push(parseInt(data[timeseries]["5. volume"]));
     }
     return {
             categoryData: categoryData.reverse(),
             price: price.reverse(),
             volume: volume.reverse(),
     };
 }
option = {
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        feature: {
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    xAxis: [
        {
            type: 'category',
            data: data0.categoryData
        }
    ],
    yAxis: [
       {
            type: 'value',
            name: 'volume',
            axisLabel: {
                formatter: '{value}'
            }
        },
        {
            type: 'value',
            name: 'price',
            axisLabel: {
                formatter: '{value}'
            }
        }
    ],
    series: [
        {
            name:'price',
            type:'line',
            yAxisIndex: 1,
            data:data0.price
        },
        {
            name:'volume',
            type:'bar',
            data:data0.volume
        }
    ]
};
 myChart.setOption(option);