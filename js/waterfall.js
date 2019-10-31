var waterfallChart={
	
	xAxisLength:0,
	yAxisLength:100,
	yAxisData:[],
	
	randomXAxisData:function() {
		
		var value = Math.floor(Math.random() * 88)-10 ;
		return value;
	},
	//初始数据
	initData:function(){
		
		waterfallChart.yAxisData=[];
		
		//[0,1,11,2,23,3,23],
		//[1,1,11,2,26,3,12],
		
		for (var i = 0; i < waterfallChart.xAxisLength; i++) {
			
			//一个dataItem
			var arr=[]
			arr.push(i);
			
			for (var j = 1; j <= waterfallChart.yAxisLength; j++) {
				arr.push(j);
				arr.push(waterfallChart.randomXAxisData());
			}
			
			
			waterfallChart.yAxisData[i]=arr;
		}
		
		//console.log(waterfallChart.yAxisData);
	},
	
	//图标默认配置
    chartOption:{
		animation: false,
		grid:{
			x:50,
			y:0,
			x2:25,
			y2:25,
		},
		backgroundColor: '#1a5d66',
		tooltip: {
			trigger: 'axis',
	 
			axisPointer: {
				animation: false
			}
		},
		xAxis: {
			show:false,
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
				show: false
			},
			type: 'category',
			splitLine: {
				show: false
			}
		},
		yAxis: {
			show:false,   
			splitLine: {
			  show: false
			},
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
			inverse:true,
			type: 'value'
		},
		series: [{
			smooth: true,
			lineStyle:{
				color:'#23a3b7'
			},
			yEhoverAnimation: false,
			showSymbol: false,
			type: 'custom',
			renderItem:function(params, api) {
		
				// 对于 data 中的每个 dataItem，都会调用这个 renderItem 函数。
				var dataIndex = params.dataIndex;
				var length = waterfallChart.xAxisLength;
				
				//console.log("dataIndex:"+dataIndex);
				
				var itemList = waterfallChart.yAxisData[dataIndex];
				
				var dateItem = [];
				for(var i=0;i<(itemList.length-1)/2;i++){
					dateItem[i] = [itemList[i*2+1],itemList[i*2+2]];
				}
				
				//console.log("dateItem:"+dateItem)
			
				var unitBandWidth = api.size([0, 0])[0] * 0.85 /(length - 1);

				//console.log("unitBandWidth:"+unitBandWidth);
				
				var hzArr = echarts.util.map(dateItem, function (entry, index) {
					return dateItem[index][1];
				});
				
				//console.log("hzArr:"+hzArr);
				
				//var maxX = Math.max.apply(Math,hzArr);

				var points = echarts.util.map(dateItem, function (entry, index) {
				
					//单个dataItem Y轴
					var value = dateItem[index][0];
					var point = api.coord([dataIndex, value]);
					
					var xvalue = dateItem[index][1];
					
					var offset = (-dataIndex/2)*unitBandWidth +(xvalue * unitBandWidth)/12;
					
					//x轴偏移
					point[0] += offset;
					
					return point;
				});

				//console.log("points："+points)

				return {
					type: 'polyline',
					shape: {
						points: points
					},
					style: api.style({
						fill: null,
						stroke: api.visual('color'),
						lineWidth: 2,
						smooth: true,
					})
				};
			}
			
			,encode: {
			        x: 0
			}
		}]
	},
	
	initChart:function(xAxisData){
		
		var myChart = echarts.init(document.getElementById('waterfallChart'));
		waterfallChart.xAxisLength=xAxisData.length;
		waterfallChart.initData();
		waterfallChart.chartOption.xAxis.data = xAxisData;
		waterfallChart.chartOption.series[0].data = waterfallChart.yAxisData;
		
		var yarr=[];
		for(var j=1;j<waterfallChart.yAxisLength;j=j+2){
			yarr.push(j);
		}
		waterfallChart.chartOption.series[0].encode.y=yarr;
	
		myChart.setOption(waterfallChart.chartOption);
		
		//console.log(waterfallChart.yAxisData)
		
		//定时刷新
	
		setInterval(function () {
		 
		 	for (var i = 0; i < waterfallChart.xAxisLength; i++) {
				
				var itemList = waterfallChart.yAxisData[i];
				itemList.splice(1, 0,1,waterfallChart.randomXAxisData());
					
				for(var j=3;j<itemList.length;j=j+2){
					var tmp = itemList[j];
					itemList[j]=tmp+1;
				}
				
				itemList.splice(itemList.length-2,2);
			}
			
			//console.log(waterfallChart.yAxisData)
			
			//waterfallChart.yAxisData.shift();
			//waterfallChart.yAxisData.push(waterfallChart.randomItem());
			
			myChart.setOption({
			    series: [{
			        data: waterfallChart.yAxisData
			    }]
			});
		 
		}, 1000);
		
	}
}