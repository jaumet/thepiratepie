package includes
{
	import mx.core.Application;
	import mx.core.UIComponent;
	import mx.rpc.events.ResultEvent;
	
	public class Wizard extends UIComponent
	{
		// sediment layers
		//private var layers:Object;
		
		// chart bounds
		private var startTime:Number;
		private var endTime:Number;
		private var top:Number;
		
		public function Wizard(width:Number, height:Number)
		{
			super();
			
			this.width  = width;
			this.height = height;
			this.x = this.y = 0;
			
			this.graphics.beginFill(0, 0.5);
			this.graphics.drawRect(0, 0, this.width, this.height);
			
			//layers = new Object();
			

			
			//Application.application.bytesRequest.send();
			Application.application.progressBar.visible = true;
			
			//this.receiveWizardData(null);
			
			this.draw();
		}
		
		public function receiveWizardData(e:ResultEvent):void
		{
			
			while(this.numChildren > 0)
			{
				this.removeChildAt(0);
			}
			
			trace("numChildren after removal: ", this.numChildren);
			
			var sampleRows:Array = String(e.result).split("\n");
			
			//var pirateData = new PirateData();
			//var sampleRows:Array = pirateData.csvString.split("\n");
	
	
			var bytesSums:Array = new Array();
			var sum:Number = 0;
			
			var lastLayerKey:String = null;
			
			this.startTime = -1.0;
			this.endTime = -1.0;
			
			
			var times:Array = new Array();
			var cats:Object = new Object();
			for(var s:int = 0; s < sampleRows.length; s++)
			{
				var sample:Array = sampleRows[s].split(",");
				
				var cat:String = sample[0];
				var time:Number = sample[1];
				var value:Number = sample[2] / 1073741824; // bytes to gigabytes
				
				if(times.indexOf(time) < 0)
					times.push(time);
				
				if( ! cats[cat] )
					cats[cat] = new Object();
				
				cats[cat][time] = value;
			}
			times.sort();
			
			
			var samplesByTime:Object = new Object();
			//for(var s:int = 0; s < sampleRows.length; s++)
			for(var keyObj:Object in cats)
			{
				for(var t:int = 0; t < times.length; t++)
				{
					//var sample:Array = sampleRows[s].split(",");
					
					var key:String = String(keyObj);
					var time = times[t];
					var value:Number;
					
					if(cats[key][time])
						value = cats[key][time];
					else
						value = 0.0;
					
					//var key:String = sample[0];
					//var value:Number = sample[2] / 1073741824; // bytes to gigabytes
		
					if(key == '')
						continue;
		
					var layer:WizardLayer;
		
					//trace(sample[0]);
					if( ! this.getChildByName(key) )
					{
						var grey:Number = Number(key) / 700.0;
						var color:uint = 0xFF0000 * grey + 0x00FF00 * grey + 0x0000FF * grey;
						
						layer = new WizardLayer(color, this.width, this.height, lastLayerKey);
						layer.name = key;
						
						this.addChild(layer);
						lastLayerKey = key;
					}
	
					if(this.startTime < 0.0 || time < this.startTime)
						this.startTime = time;
					if(this.endTime < 0.0 || time > this.endTime)
						this.endTime = time;
					
					layer.pushSample(time, value);
				}
			}
			
			top = this.getMaxHeight();
			
			trace(top);
			
			this.draw();
			
			Application.application.startTimeLabel.text = this.unix2date(this.startTime);
			Application.application.endTimeLabel.text   = this.unix2date(this.endTime);
			Application.application.topValueLabel.text  = String(Math.floor(this.top)) + " GB";
			Application.application.bottomValueLabel.text="0 GB";
			Application.application.progressBar.visible = false;
	
	
		}
		
		private function unix2date(timestamp_in_seconds:Number):String
		{
			//unix timestamp -> human date
			var currDate:Date = new Date(timestamp_in_seconds*1000); //timestamp_in_seconds*1000 - if you use a result of PHP time function, which returns it in seconds, and Flash uses milliseconds
			    
			var D:Number = currDate.getDate();
			var M:Number = currDate.getMonth()+ 1; //because Returns the month (0 for January, 1 for February, and so on)
			var Y:Number = currDate.getFullYear();
			
			return String(D + "." + M + "." + Y);
		}
		
		public function getMaxHeight():Number
		{
			if(this.numChildren < 1)
				return 1.0;
			
			var max:Number = 0.0;
			
			for(var c:int = 0; c < this.numChildren; c++)
			{
				var h:Number = WizardLayer(this.getChildAt(c)).getMaxHeight();
				if(h > max)
					max = h;
			}
			
			return WizardLayer(this.getChildAt(this.numChildren-1)).getMaxHeight();
		}
		
		public function getLayerWithKey(key:String):WizardLayer
		{
			if(key == null)
				return null;
				
			return WizardLayer(this.getChildByName(key));
		}
		
		public function draw():void
		{
			this.graphics.beginFill(0xDDDDDD, 1.0);
			this.graphics.drawRect(0, 0, this.width, this.height);
			this.graphics.endFill();
			
			for(var c:int = 0; c < this.numChildren; c++)
			{
				WizardLayer(this.getChildAt(c)).draw(this.startTime, this.endTime, 0.0, top);
			}
			
			/*
			for(var key:String in layers)
			{
				layers[key].draw(this.graphics);
			}
			*/
		}

	}
}