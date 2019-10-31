var lineChart={

	xAxisData:[],
	yAxisData:[],
    baseCategory:100,

	randomXAxisData:function() {
	
		var step =  Math.max(Math.random() * 3,0.4);
		//console.log("step:"+step)
		lineChart.baseCategory = lineChart.baseCategory+step ;
		var category = parseFloat(lineChart.baseCategory).toFixed(1);
		return category;
	},

	randomYAxisData:function() {
		
		var value = Math.floor(Math.random() * 88)-50 ;
		return value;
	},
	
	//初始数据
	initData:function(){
	
		lineChart.xAxisData = [];
		lineChart.yAxisData=[];
		
		for (var i = 0; i < 20; i++) {
			lineChart.xAxisData.push(lineChart.randomXAxisData()+'M');
			lineChart.yAxisData.push(lineChart.randomYAxisData());
		}
		
	},

	//图标默认配置
    chartOption:{
		//animation: false,
		grid:{
			x:50,
			y:25,
			x2:25,
			y2:25,
		},
		tooltip: {
			trigger: 'axis',
	 
			axisPointer: {
				animation: false
			}
		},
		xAxis: {
			axisLabel: {
				textStyle: {
					color: '#ddd'
				}
			},
			axisLine: {
				lineStyle: {
					color: '#ddd'
				}
			},
			axisTick: {
				show: true
			},
			type: 'category',
			splitLine: {
				show: false
			}
		},
		yAxis: {
			   
			axisLine: {
				show: false
			},
			axisTick: {
				show: false
			},
			axisLabel: {
				textStyle: {
					color: '#ddd'
				}
			},

			type: 'value'
		},
		series: [{
			smooth: true,
			lineStyle:{
				color:'#23a3b7'
			},
			type: 'line',
			showSymbol: false,
			yEhoverAnimation: false
		}]
	},
	
	initChart:function(){
		
		var myChart = echarts.init(document.getElementById('lineChart'));
		lineChart.initData();
		lineChart.chartOption.xAxis.data = lineChart.xAxisData;
		lineChart.chartOption.series[0].data = lineChart.yAxisData;
		
		myChart.setOption(lineChart.chartOption);
		
		
		//定时刷新
		setInterval(function () {
		
		    for (var i = 0; i < 5; i++) {
				//xAxisData.shift();
				lineChart.yAxisData.shift();
				//xAxisData.push(randomXAxisData());
				lineChart.yAxisData.push(lineChart.randomYAxisData());
				
		    }
			
			myChart.setOption({
				// xAxis:{
				// 	data:xAxisData
				// },
			    series: [{
			        data: lineChart.yAxisData
			    }]
			});
		 
		}, 1000);
		
	}
}