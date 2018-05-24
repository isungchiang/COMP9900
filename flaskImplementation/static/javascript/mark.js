 var myChart = echarts.init(document.getElementById('mark'));
 var mark_time;
 var time;
 var stockid = $("#StockID").data("result");
 var id ;
 var contentlist = ['',''];
 var jason;
 var lables;
 var content = ''
 $.ajax({
    async: false,
    url: 'http://comp9900fafafa.azurewebsites.net/api/BasicInfo/GetStat?stockId='+stockid,
    success: function (stock_data) {
        id = stock_data[0]['StockId'];
        jason = strToJson(stock_data[0]['json']);

        mark_time  = get_mark_time(jason);
        // time = json['last_refresh_date'];
    }
 });
 lables = jason['marks'][mark_time.time]['labels']
// console.log(lables)
for (i in lables){
     // console.log(lables[i]['labels'])
     if (lables[i]['labels'] == 1){
         contentlist[1]+=lables[i]['content']+'</br>'
     }else {
         contentlist[0]+=lables[i]['content']+'</br>'
     }

}
// console.log(contentlist)
 // for (i in contentlist){
 //    content += contentlist[i]+'</br>'
 // }

function strToJson(str) {

    var json = eval('(' + str + ')');
    return json;
}
function get_mark_time(json) {
    var time = json['last_refresh_date'];
    var mark = parseFloat(json['marks'][time]['mark']);



    // console.log(mark);
    return {
        mark:mark.toFixed(1),
        time:time,
    };
}

function suggestion(mark) {
    if(mark>5){
        return "Positive recommendation"
    }else{
        return "Negative recommendation"
    }

}


// console.log(mark_time.mark)

option = {
    title: {
        text: mark_time.mark,
        textStyle:{
            color:'#d75442',
            fontSize:40,
        },
        x: 'center',
        y: 'center'
   },
    tooltip: {
        show:false,
        trigger: 'item',
        // formatter: "{a} <br/>{b}: {c} ({d}%)"
        // formatter:content,
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data:['negative','positive']
    },
    color:['#54d6b6','#de502b'],
    series: [
        {
            name:'',
            type:'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            // hoverAnimation:false,
            // silent:true,
            label: {
                normal: {
                    show: false,
                    position: 'center',
                    // formatter:function () {
                    //     return'7'
                    // },
                    // textStyle:{
                    //     fontSize:40,
                    //     color:'#d75442'
                    // }
                },
                emphasis: {
                    show: true,
                    textStyle: {
                        fontSize: '30',
                        fontWeight: 'bold'
                    }
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data:[
                {value:mark_time.mark*10, name:''},
                {value:100-mark_time.mark*10, name:''}

            ]
        }
    ]
};
 myChart.setOption(option);