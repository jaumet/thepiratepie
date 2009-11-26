package includes
{
	import flash.display.Sprite;





	public class WizardLayer extends Sprite
	{
		private var color:uint;
		public var wizardWidth:Number;
		public var wizardHeight:Number;
		
		private var samples:Array;
		private var samplesStartTime:Number;
		private var samplesEndTime:Number;
		
		private var previousLayerKey:String;
		
		private var lowerHeights:Array;
		
		public function WizardLayer(color:uint, wizardWidth:Number, wizardHeight:Number, previousLayerKey:String)
		{
			super();
			
			this.color = color;
			
			this.wizardWidth = wizardWidth;
			this.wizardHeight = wizardHeight;
			this.x = 0;
			this.y = 0;
			
			this.samples = new Array();
			this.previousLayerKey = previousLayerKey;
			this.lowerHeights = new Array();
			
			this.samplesEndTime = -1.0;
			this.samplesStartTime = -1.0;
			
			/*
			this.graphics.beginFill(fillColor, fillAlpha);
			this.graphics.lineStyle(lineThickness, lineColor, lineAlpha);
			var h:Number = side * Math.sin( 30 * Math.PI / 180);
			this.graphics.moveTo(0, -h / 2);
			this.graphics.lineTo( side / 2, h / 2);
			this.graphics.lineTo( -side / 2, h / 2);
			this.graphics.lineTo(0, -h / 2);
			this.graphics.endFill();
			*/
		}
		

		
		public function pushSample(time:Number, value:Number):void
		{
			if(this.samplesStartTime < 0.0 || time < this.samplesStartTime)
				this.samplesStartTime = time;
			if(this.samplesEndTime < 0.0 || time > this.samplesEndTime)
				this.samplesEndTime = time;
			
			this.samples[samples.length] = value;
			this.lowerHeights[samples.length-1] = -1.0;
		}
		
		public function getLowerHeightAtIndex(index:int):Number
		{
			
			var previousLayer:WizardLayer = Wizard(parent).getLayerWithKey(previousLayerKey);
			
			if(previousLayer == null)
				this.lowerHeights[index] = 0.0;
				
			if(this.lowerHeights[index] < 0.0)
				this.lowerHeights[index] = previousLayer.getUpperHeightAtIndex(index);
			
			return this.lowerHeights[index];
		}
		
		public function getUpperHeightAtIndex(index:int):Number
		{
			return this.getLowerHeightAtIndex(index) + getHeightAtIndex(index);
		}
		
		public function getHeightAtIndex(index:int):Number
		{
			return samples[index];
		}
		
		public function getMaxHeight():Number
		{
			var max:Number = 0;
			for(var s:int = 0; s < samples.length; s++)
			{
				if(this.getUpperHeightAtIndex(s) > max)
					max = this.getUpperHeightAtIndex(s);
			}
			return max;
		}
		
		private function time2index(time:Number):int
		{
			var fraction:Number = (time - this.samplesStartTime) / (this.samplesEndTime-this.samplesStartTime);
			return int(fraction*(samples.length-1));
		}
		
		private function samplesDuration():Number
		{
			return this.samplesEndTime - this.samplesStartTime;
		}
		
		private function rangeTransform(value:Number, fromLow:Number, fromHigh:Number, toLow:Number, toHigh:Number):Number
		{
			var fraction:Number = (value - fromLow)/(fromHigh-fromLow);
			
			return toLow + fraction * (toHigh-toLow);
		}
		
		public function draw(startTime:Number, endTime:Number, bottom:Number, top:Number):void
		{
			
			
			var visibleDuration:Number = endTime - startTime;
			
			
			var s:int;
			var time:Number;
			var visibleTimeFraction:Number;
			var x:Number;
			
			// draw bottom of slice to the right
			this.graphics.moveTo(0.0, rangeTransform(this.getLowerHeightAtIndex(0), bottom, top, this.wizardHeight, 0 ));
			this.graphics.beginFill(this.color, 0.8);
			for(s = 1; s < samples.length; s++)
			{
				time = this.samplesStartTime + this.samplesDuration() * Number(s) / Number(samples.length);
				visibleTimeFraction = (time - startTime) / visibleDuration;
				x = this.wizardWidth * visibleTimeFraction;
				
				this.graphics.lineTo(x, rangeTransform(this.getLowerHeightAtIndex(s), bottom, top, this.wizardHeight, 0 ) );
			}
			
			// draw top of slice to the left
			for(s = samples.length-1; s >= 0; s--)
			{
				time = this.samplesStartTime + this.samplesDuration() * Number(s) / Number(samples.length);
				visibleTimeFraction = (time - startTime) / visibleDuration;
				x = this.wizardWidth * visibleTimeFraction;
				
				this.graphics.lineTo(x, rangeTransform(this.getUpperHeightAtIndex(s), bottom, top, this.wizardHeight, 0 ) );
			}
			
			
			this.graphics.endFill();
			
			trace(samples.length);
			
			//trace(this.getLowerHeightAtTime(0.0));
		}
		
	}
}