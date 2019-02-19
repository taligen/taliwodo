

function recalculateWorkdownStepAges() {
    var tds = document.getElementsByTagName("td");
    for( var i=0 ; i<tds.length ; ++i ) {
        td = tds[i];
        lastupdated = td.getAttribute( 'data-lastupdated' )
        if( lastupdated ) {
            if( lastupdated != '-' ) {
                td.innerHTML = lastupdated + '<br>' + relativeTimeFrom( lastupdated );
            } else {
                td.innerHTML = '&ndash;';
            }
        }
    }
}

function workdownStepUpdated( name ) {
    var myform = document.forms['workdown_form']

    var http = new XMLHttpRequest();
    http.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            var dict = {};
            http.responseText.split( '&' ).forEach( function( pair ) {
                var pair2 = pair.split( '=', 2 );
                dict[pair2[0]] = pair2[1];
            } );

            var tr = document.getElementById( name );

            var tds = tr.getElementsByTagName("td");
            for( var i=0 ; i<tds.length ; ++i ) {
                var td = tds[i];
                if( td.hasAttribute( 'data-lastupdated' )) {
                    td.setAttribute( 'data-lastupdated', dict['lastupdated'] );
                }
            }

            recalculateWorkdownStepAges()
        }
    };

    http.open("POST", myform.action, true);
    http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    http.send('verb=updateworkdown&name=' + name + '&value=' + myform[name].value);

}

function relativeTimeFrom( ts ) {
    var match = /^(\d\d\d\d)(\d\d)(\d\d)-(\d\d)(\d\d)(\d\d)/.exec( ts );
    if( !match ) {
        return '?';
    }

    var dts = new Date( match[1], match[2]-1, match[3], match[4], match[5], match[6] );
    var now = Date.now();
    var deltaSec = Math.round( ( now - dts )/1000 );

    if( deltaSec < 60 ) {
        return "&lt; 1 min ago";
    }

    deltaMin = Math.round( deltaSec/60 );
    if( deltaMin < 60 ) {
        return "&asymp; " + deltaMin + " min ago";
    }

    deltaHour = Math.round( delta.Min/60 );
    if( deltaHour < 24 ) {
        return "&asymp; " + deltaHour + " h ago";
    }

    deltaDay = Math.round( deltaHour/30 );
    return "&asymp; " + deltaDay + " d ago";
}

window.onload = function() {
    recalculateWorkdownStepAges()
}
