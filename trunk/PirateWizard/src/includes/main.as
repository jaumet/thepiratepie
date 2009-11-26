// ActionScript file

import flash.events.Event;

import includes.Wizard;

import mx.rpc.events.ResultEvent;

var wizard:Wizard;

private function makeWizard(e:Event):void
{
	wizard = new Wizard(canvas.width, canvas.height);
	canvas.addChild(wizard);
}

private function receiveWizardData(e:ResultEvent):void {
	wizard.receiveWizardData(e);
}

private function requestCategories(e:Event):void
{
	categoriesRequest.send();
}

private function receiveCategories(e:ResultEvent):void {
	//Alert.show(String(e.result));

/* 	var csvString:String = String(e.result);
	var rows:Array = csvString.split("\n");
	
	for(var r:int = 0; r < rows.length-1; r++) {
		var cat:Array = rows[r].split(',');
		
		var catBox:CheckBox = new CheckBox();
		catBox.label = cat[1];
		catBox.height = 10;
		categorySelection.addChild(catBox);
		
	} */
	

	
	
}