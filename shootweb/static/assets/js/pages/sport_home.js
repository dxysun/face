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



    var myRelationship = echarts.init(document.getElementById('relationship'));
    var myAttention = echarts.init(document.getElementById('attention'));


    myRelationship.setOption(option_relationship);
    myAttention.setOption(radar_option_attention);

});