// ActionScript file

import flash.events.Event;

import includes.PirateData;
import includes.Wizard;

import mx.controls.TextInput;
import mx.rpc.events.FaultEvent;
import mx.rpc.events.ResultEvent;
import mx.rpc.http.HTTPService;

var wizard:Wizard;

private function doSearch(e:Event):void
{
	Application.application.progressBar.visible = true;
	
	var textInput:TextInput = TextInput(e.target);
	trace(textInput.text);
	
	
/*
(
`title` LIKE '%curb%'
)
AND (
`title` LIKE '%your%'
)
AND (
`title` LIKE '%enthusiasm%'
)
*/	
	var words:Array = textInput.text.split(" ");
	
	var parameters:Object = new Object();
	parameters["query"] = "SET @bins =100; SET @bin_size = ( SELECT (MAX( date ) - MIN( date ) ) / @bins FROM torrentinfo); SELECT cat, FLOOR( torrentinfo.date / @bin_size )*@bin_size AS `date` , SUM( size ) AS size FROM `torrentinfo` WHERE ";
	for(var w:Object in words)
	{
		parameters["query"] += (w > 0 ? " AND " : "") + " (`title` LIKE '%" + words[w] + "%') ";
	}
	parameters["query"] += " GROUP BY FLOOR( torrentinfo.date / @bin_size ), torrentinfo.cat ORDER BY torrentinfo.cat ASC, date ASC";
	
	trace(parameters["query"]);
	
    var service:HTTPService = new HTTPService();
    //service.destination = "sampleDestination";
    service.useProxy = false;
    service.rootURL = "http://www.thepiratepie.org/wizard/sql.py";
    service.url = "http://www.thepiratepie.org/wizard/sql.py";
    service.method = "POST";
    service.addEventListener("result", receiveWizardData);
    service.addEventListener("fault", httpFault);
    service.send(parameters);

}

private function httpFault(e:FaultEvent):void
{
	trace(e.fault.faultDetail, e.fault.faultString);
}

private function makeWizard(e:Event):void
{
	wizard = new Wizard(canvas.width, canvas.height);
	canvas.addChild(wizard);
	
	var pirateData:PirateData = new PirateData();
	var ev:ResultEvent = new ResultEvent("cached result", false, true, pirateData.csvString);
	
	Application.application.progressBar.visible = true;
	wizard.receiveWizardData(ev);
}

private function receiveWizardData(e:ResultEvent):void {
	trace("hello from receiveWizardData");
	wizard.receiveWizardData(e);
}

/* private function requestCategories(e:Event):void
{
	categoriesRequest.send();
} */

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