/**
 * Created by lenovo on 2018/5/20.
 */
$(function () {

    var data1 = [];
    var data_grade = [];
    var data_index = [];
    for (var i = 0; i < 60; i++) {
        data1.push([(10 - Math.random() * 5).toFixed(1), (Math.random() * 360).toFixed(1)]);
        data_grade.push((10 - Math.random() * 5).toFixed(1));
        data_index.push(i + 1);

    }

    var option_relationship = {
        title: {
            textStyle: {
                fontSize: 34,
                fontStyle: 'normal',
                fontWeight: 'normal'
            },
            text: '成绩与其他因素关系图',
            x: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {
                    show: true,
                    readOnly: true
                },
                magicType: {
                    show: true,
                    type: ['line', 'bar']
                },
                restore: {
                    show: true
                },
                saveAsImage: {
                    show: true
                }
            }
        },
        calculable: false,
        xAxis: [{
            type: 'category',
            name: '相关因素',
            axisLabel: {
                interval: 0
            },
            data: ['手部', '肩部', '腰部', '臂部', '心率', '速射时间', '时间节奏', '紧张度', '放松度', '专注度', '疲劳程度'],

        }],
        yAxis: [{
            type: 'value',
            name: '相关系数'
        }],
        series: [{
            name: '相关系数',
            type: 'bar',
            data: [3.2, 2.4, 1.5, 2.8, 1.3, 0.4, 0.5, -1.3, 2, 3, -2.2],
            markPoint: {
                data: [{
                    type: 'max',
                    name: '最大值'
                }, {
                    type: 'min',
                    name: '最小值'
                }]
            }

        }
        ]
    };

    var legendData = ['运动员1', '运动员2', '运动员3', '运动员4'];

    var serieData = [];
    var metaDate = [];
    var xAxisData = [];
    var Max = 600;
    var Min = 400;
    for (var k = 0; k < 4; k++) {
        var data = [];
        for (var j = 0; j <= 10; j++) {
            var Range = Max - Min;
            var Rand = Math.random();
            var num = Min + Math.round(Rand * Range); //四舍五入
            data.push([j, num.toFixed(2)]);
        }
        metaDate.push(data);
    }
    for (var p = 0; p < 10; p++) {
        xAxisData.push(p + 1);
    }
    for (var v = 0; v < legendData.length; v++) {
        var serie = {
            name: legendData[v],
            type: 'line',
            smooth: true,
            data: metaDate[v]
        };
        serieData.push(serie)
    }


    var option = {
        title: {
            text: '运动员成绩变化图'
        },
        tooltip: {
            trigger: 'axis'
            // triggerOn: 'mousemove',
            // triggerOn: 'none',
            // formatter: function (params) {
            //     return params.data[1].toFixed(0);
            // }
        },
        legend: {
            x: 'left',
            y: 'middle',
            orient: 'vertical',
            data: legendData
        },
        dataZoom: {
            show: true,
            realtime: true

        },
        grid: {
            left: '100px;',

            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            name: '比赛场次',
            type: 'category',
            boundaryGap: false,
            data: xAxisData
        },
        yAxis: {
            name: '比赛成绩',
            type: 'value'
        },
        series: serieData
    };


    var myRelationship = echarts.init(document.getElementById('relationship'));
    var myChart = echarts.init(document.getElementById('myChart'));


    myRelationship.setOption(option_relationship);
    myChart.setOption(option);

});