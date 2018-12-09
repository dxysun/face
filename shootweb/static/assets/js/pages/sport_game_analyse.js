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

    var options = {
        title: {
            text: '射击数据图示',
            left: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} : {c}'
        },
        legend: {
            data: ['射击点'],
            top: 40
        },
        polar: {
            radius: 170
        },
        angleAxis: {
            type: 'value'
        },
        radiusAxis: {
            //    axisAngle: 0,
            min: 0,
            max: 10,
            interval: 1,
            inverse: true
        },
        dataZoom: [
            {
                type: 'slider',
                radiusAxisIndex: 0,
                bottom: 40,
                start: 0,
                end: 100
            },
            {
                type: 'inside',
                radiusAxisIndex: 0,
                start: 0,
                end: 100
            }
        ],
        series: [{
            coordinateSystem: 'polar',
            // FIXME
            // 现在必须得设置这个，能不能polar和catesian一样，要不然很多特殊处理。
            angleAxisIndex: 0,
            radiusAxisIndex: 0,
            name: '射击点',
            type: 'scatter',
            symbolSize: 5,
            data: data1
        }]
    };

    var data_level = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    var data_total = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    data_grade.forEach(function (item, index) {

        data_total[Math.floor(item) - 1]++;
    });

    var total_grade = {
        color: ['#3398DB'],
        title: {
            left: 'center',
            text: '成绩统计图'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            name: '环数',
            data: data_level,
            axisTick: {
                alignWithLabel: true
            }
        }],
        yAxis: [{
            type: 'value',
            name: '次数'
        }],
        series: [{
            name: '次数',
            type: 'bar',
            barWidth: '50%',
            data: data_total
        }]
    };

 //   var legendData = ['手部', '肩部', '腰部', '臂部'];
    var legendData = ['x方向', 'y方向'];
    var title = "抖动数据折线图";
    var serieData = [];
    var metaDate = [];
    var xAxisData = [];
   // 10-21-23.txt
   var xData = [
        2.750,0.500,0.250,0.250,0.000,0.000,0.000,0.000,0.000,0.000,-0.250,0.000,0.000 ,
        0.000,0.000,0.000,-0.250,2.250,0.750,0.750,0.500,0.250,0.250,0.000,0.000,0.000,0.000,0.000,-0.250,0.000,0.000,0.000,-0.250,
        0.000,0.000,0.250,0.000,0.000,0.000,-0.250,2.500,1.000,1.000,0.250,0.500,0.250,0.000,0.000,0.000,0.000,-0.250,0.000,-0.250,
        -0.250,0.000,0.000,0.000,0.000,-0.250,0.000,1.500,1.000,0.750,0.750,0.250,0.000,0.000,0.250,0.000,0.000,0.000,0.000,
        0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,1.000,1.250,1.000,0.500,0.250,0.250,0.000,0.000,0.250,0.000,0.500,
        0.000,0.250,0.250,0.250,0.000,0.250,0.250,0.000,-0.250,-0.250,-1.000,-1.750,-2.750,-1.500,-18.750
    ];
    var yData =[
        0.000,0.000,-0.250,-0.250,-0.500,-0.250,-0.500,0.000,-0.250,-0.250,0.000,-0.250,0.000,
         -0.250,0.000,-0.250,0.000,4.000,0.250,0.000,0.250,0.250,-0.500,-0.250,-0.250,-0.500,-0.500,-0.250,-0.500,-0.250,-0.250,0.000,-0.250,
        0.000,0.000,-0.250,0.000,0.000,0.000,-0.250,4.250,0.000,-0.250,0.000,-0.500,-0.750,-0.500,-0.250,-0.500,-0.500,-0.500,-0.250,-0.250,
        -0.250,0.000,0.000,-0.250,0.000,0.000,0.000,2.250,2.000,-0.500,0.250,-0.250,-0.500,-0.250,-0.250,-0.250,-0.500,0.000,-0.500,
        -0.500,-0.250,-0.250,0.000,-0.250,-0.250,0.000,0.000,0.000,0.750,2.750,-0.250,1.000,0.250,0.250,0.250,0.000,-0.250,-0.250,-0.250,
        -0.500,-0.500,-0.500,-0.500,-0.250,-0.250,-0.250,0.000,0.000,0.000,-1.000,-3.500,-8.000,-10.000,18.750
    ];
   /*// 10-23-43.txt
    var xData = [
        0.000,0.000,-0.250,0.000,-0.250,0.000,-0.250,0.000,-0.250,-0.250,2.250,1.000,0.500,0.500,
        0.250,0.250,0.000,0.000,0.250,0.000,0.000,0.000,0.000,0.000,0.000,-0.250,0.000,1.500,1.250,0.750,0.750,0.750,0.250,
        0.500,0.000,0.000,0.250,0.000,-0.250,0.000,0.000,0.000,0.000,-0.500,2.250,1.000,0.500,0.750,0.250,0.250,0.000,0.250,-0.250,
        0.000,0.000,0.000,-0.250,0.000,0.000,-0.250,1.500,1.000,0.750,0.500,0.500,0.250,0.000,0.500,0.000,0.000,0.250,-0.250,0.000,
        -0.250,-0.250,-0.500,-1.000,-1.500,-1.750,-18.750,-11.000
    ];
    var yData =[
         -1.750,-0.250,-0.250,0.000,0.000,0.000,0.000,0.000,0.000,-0.250,4.250,0.000,-0.250,-0.250,
        0.000,-0.500,0.000,-0.250,-0.250,-0.500,0.000,-0.500,-0.250,-0.250,-0.250,-0.500,0.000,2.250,2.000,-0.250,0.000,0.000,-0.250,
        -0.750,-0.500,-0.500,-0.250,-0.500,-0.250,-0.250,-0.250,0.000,0.250,-0.250,4.750,1.000,-0.500,-0.250,0.000,-1.000,-0.500,-0.750,-1.000,
        -0.500,-0.250,-0.500,-0.250,0.000,0.000,0.000,2.750,1.750,-0.250,0.000,0.250,0.000,0.000,-0.500,-0.500,-0.500,-0.500,-0.500,-0.750,
        -0.250,0.000,0.250,-0.500,-2.750,-4.250,5.250,-2.250
    ];*/
/*
    //10-25-46.txt
    var xData = [
        0.750,-0.250,0.000,0.000,0.000,-0.250,0.000,0.000,0.000,-0.250,2.250,0.750,1.000,0.500,0.500,0.250,0.500,0.000,0.250,0.000,
        0.000,0.000,0.000,-0.250,0.000,0.000,0.000,-0.250,2.000,0.500,0.500,0.250,0.500,0.000,0.250,0.000,0.000,0.000,0.000,
        0.000,0.000,0.000,0.250,0.000,-0.250,0.000,2.000,1.000,1.000,0.500,0.250,0.250,0.250,0.000,0.000,-0.250,-18.750,0.000,-18.000,
        -10.750,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,
        0.000,0.000,0.000
    ];
    var yData =[
        -1.500,-0.500,-0.250,-0.250,-0.250,-0.250,0.000,0.000,-0.250,-0.500,4.000,0.250,-0.250,0.000,-0.500,-0.250,0.000,-0.250,-0.250,-0.250,
        -0.500,-0.250,-0.250,-0.250,0.250,-0.250,0.000,0.000,3.500,-0.500,-0.250,0.000,-0.500,-0.750,-0.250,-0.500,-0.250,0.000,-0.250,
        0.000,-0.250,0.000,0.000,0.000,0.000,-0.250,3.500,0.750,-0.500,-0.250,-0.250,-0.500,-0.500,-0.500,-0.500,0.000,18.750,8.500,17.250,
        7.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,
        0.000,0.000,0.000
    ];*/
  /* // 10-35-00.txt
   var xData = [
        3.000,0.500,0.500,0.250,0.250,0.000,0.250,-0.250,-0.250,
        1.250,0.750,0.750,1.250,0.500,0.250,0.000,0.000,-0.250,-1.000,1.250,1.000,0.500,0.250,1.000,0.250,0.000,
        0.250,0.000,-0.500,-0.250,1.500,1.000,0.500,0.000,0.500,0.250,0.250,0.000,0.000,0.000,0.000,-0.250,-0.250,-0.250,-0.250,
        -1.000,-0.500,0.000,1.500,4.750
    ];
    var yData =[
        2.750,-0.250,-0.500,-0.250,-0.250,-0.250,-0.250,-0.250,0.250,
        1.500,1.750,-0.250,0.500,-1.000,-0.500,-0.500,-0.750,-0.750,-0.250,3.000,-0.250,-0.500,-0.250,-1.250,-0.500,-0.250,
        -0.750,-0.250,0.250,-0.250,4.000,-0.250,0.750,0.250,-0.250,-0.500,-0.500,-0.500,-0.500,-0.750,-0.750,0.000,0.000,-0.250,0.250,
        -0.250,-0.750,-3.750,-5.500,-15.250
    ];*/
    var len = xData.length ;
    metaDate.push(xData);
    metaDate.push(yData);
/*    for (var k = 0; k < 2; k++) {
        var data = [];
        var d = 0;
        for (var j = 0; j < 60; j++) {
            var t = Math.random() * 10 - 5 ;

            data.push(t.toFixed(2));
            d = d + t;
        }
        // pie_data[k] = (d / 60).toFixed(2);
        metaDate.push(data);
    }*/
    for (var p = 0; p < len; p++) {
        xAxisData.push(p + 1);
    }
    for (var v = 0; v < legendData.length; v++) {
        var serie = {
            name: legendData[v],
            type: 'line',
            symbol: "circle",
            symbolSize: 10,
            data: metaDate[v]
        };
        serieData.push(serie)
    }
    var colors = ["#036BC8", "#4A95FF", "#5EBEFC", "#2EF7F3", "#FFFFFF"];
    var option_line_shake = {
        backgroundColor: '#0f375f',
        title: {
            text: title,
            textAlign: 'left',
            textStyle: {color: "#fff", fontSize: "16", fontWeight: "normal"}
        },
        legend: {
            show: true, left: "right", data: legendData, y: "5%",
            itemWidth: 18, itemHeight: 12, textStyle: {color: "#fff", fontSize: 14},
        },
        dataZoom: {
            show: true,
            realtime: true,
            start: 0,
            end: 100
        },
        color: colors,
        grid: {left: '2%', top: "12%", bottom: "5%", right: "5%", containLabel: true},
        tooltip: {trigger: 'axis', axisPointer: {type: 'shadow'}},
        xAxis: [
            {
                type: 'category',
                axisLine: {show: true, lineStyle: {color: '#6173A3'}},
                axisLabel: {interval: 0, textStyle: {color: '#9ea7c4', fontSize: 14}},
                axisTick: {show: false},
                data: xAxisData
            }
        ],
        yAxis: [
            {
                axisTick: {show: false},
                splitLine: {show: false},
                axisLabel: {textStyle: {color: '#9ea7c4', fontSize: 14}},
                axisLine: {show: true, lineStyle: {color: '#6173A3'}},
            }
        ],
        series: serieData
    };

     var pie_data = [0, 0, 0, 0];
     for (var p1 = 0; p1 < 4; p1++) {

        var d1 = 0;
        for (var j1 = 0; j1 < 60; j1++) {
            var t1 = Math.random() * 10 ;
            d1 = d1 + t1;
        }
        pie_data[p1] = (d1 / 60).toFixed(2);

    }
    var option_pie = {
        title: {
            text: '抖动数据统计',
            x: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['手部', '肩部', '腰部', '臂部']
        },
        series: [
            {
                name: '平均抖动幅度占比',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: [
                    {value: pie_data[0], name: '手部'},
                    {value: pie_data[1], name: '肩部'},
                    {value: pie_data[2], name: '腰部'},
                    {value: pie_data[3], name: '臂部'}
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    var values = [];
    var Max = 60;
    var Min = 40;
    for (k = 0; k < 60; k++) {
        var Range = Max - Min;
        var Rand = Math.random();
        var num = Min + Math.round(Rand * Range); //四舍五入
        values.push(num);
    }
    var option_heart = {
        title: {
            text: '心率变化数据'
        },
        tooltip: {
            triggerOn: 'onmousemove',
            formatter: function (params) {
                return '次数: ' + params.name + '<br>心跳: ' + params.value + '次';
            }
        },
        dataZoom: {
            show: true,
            realtime: true,
            start: 0,
            end: 20
        },
        xAxis: {
            boundaryGap: false,
            data: xAxisData,
            axisLabel: {
                color: '#000000'
            },
            axisLine: {
                lineStyle: {
                    color: '#BFBFBF'
                }
            }
        },
        yAxis: {
            axisLabel: {
                color: '#000000'
            },
            axisLine: {
                lineStyle: {
                    color: '#BFBFBF'
                }
            }
        },
        series: [{
            type: 'line',
            data: values,
            color: ['#2F42FF'],
            symbolSize: 10,
            label: {
                normal: {
                    show: true//圆点上显示值
                }
            },
            markLine: {
                data: [{
                    type: 'average',
                    name: '平均值'
                }]
            }
        }]
    };

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

    var radar_option_attention = {
        title: {
            text: '技能图'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            x: 'center',
            data: ['技能点', '稳定性', '成绩水平', '心态']
        },
        radar: {
            indicator: [{
                text: '稳定性',
                max: 10
            },
                {
                    text: '成绩水平',
                    max: 10
                },
                {
                    text: '心态',
                    max: 10
                }

            ],
            center: ['50%', '50%'],
            radius: 130
        },
        series: {
            type: 'radar',
            tooltip: {
                trigger: 'item'
            },
            itemStyle: {
                normal: {
                    areaStyle: {
                        type: 'default'
                    }
                }
            },
            data: [{
                value: [6, 7, 8],
                name: '技能点'
            }]
        }
    };


    var option_grade = {
        title: {
            left: 'center',
            text: '成绩趋势走向图'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                animation: false
            }
        },
        legend: {
            data: ['射击成绩'],
            top: 25
        },
        axisPointer: {
            link: {
                xAxisIndex: 'all'
            }
        },
        dataZoom: {
            show: true,
            realtime: true,
            start: 40,
            end: 60,
            xAxisIndex: [0, 1]
        },
        grid: [{
            left: 40,
            right: 40
        }, {
            left: 40,
            right: 40
        }],
        xAxis: [{
            type: 'category',
            boundaryGap: true,
            axisLine: {
                onZero: true
            },
            name: '次数',
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#fcc',
                    width: 1
                }
            },
            data: data_index
        }, {
            gridIndex: 1
        }],
        yAxis: [{
            type: 'value',
            max: 10,
            name: '环数',
            min: 0,
            interval: 2,
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#fcc',
                    width: 2
                }
            }
        }, {
            gridIndex: 1
        }],
        series: [{
            name: '环数',
            type: 'line',
            smooth: true,
            itemStyle: {
                normal: {
                    color: '#f94427'
                }
            },

            data: data_grade
        }]
    };
    var myGrade = echarts.init(document.getElementById('grade'));
    var myChart = echarts.init(document.getElementById('circle'));
    var myTotalGrade = echarts.init(document.getElementById('total_grade'));
    var myLineShake = echarts.init(document.getElementById('line_shake'));
  //  var myTotalShake = echarts.init(document.getElementById('total_shake'));
    var myHeart = echarts.init(document.getElementById('heart'));
   // var myRelationship = echarts.init(document.getElementById('relationship'));
  //  var myAttention = echarts.init(document.getElementById('attention'));

    myChart.setOption(options);
    myGrade.setOption(option_grade);
    myTotalGrade.setOption(total_grade);
    myLineShake.setOption(option_line_shake);
 //   myTotalShake.setOption(option_pie);
    myHeart.setOption(option_heart);
  //  myRelationship.setOption(option_relationship);
  //  myAttention.setOption(radar_option_attention);

});