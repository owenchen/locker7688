var mcs = require('mcsjs');


var myApp = mcs.register({
deviceId: 'DhBfDohn',
deviceKey: 'BhYcxoK07FBeAgcV',
});

console.log("myApp Setup:");
console.log(myApp);

console.log(myApp.on);

console.log("MCS alloc:");
console.log(mcs);
console.log("================")

console.log(myApp.on);


myApp.on('LED_control', function(data, time) {
  if(Number(data) === 1){                     
    console.log('blink');
    console.log(time);
  } else {
    console.log('off');
  }


});
