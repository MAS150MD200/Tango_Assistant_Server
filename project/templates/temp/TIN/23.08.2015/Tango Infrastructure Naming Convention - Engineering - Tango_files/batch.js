try {
AJS.Confluence.SharePage={};
AJS.Confluence.SharePage.autocompleteUser=function(C){C=C||document.body;
var D=AJS.$,A=/^([a-zA-Z0-9_\.\-\+\!#\$%&'\*/=\?\^_`{|}~])+\@.*/;
var B=function(F){if(!F||!F.result){throw new Error("Invalid JSON format")
}var E=[];
E.push(F.result);
return E
};
D("input.autocomplete-sharepage[data-autocomplete-user-bound!=true]",C).each(function(){var G=D(this).attr("data-autocomplete-sharepage-bound","true").attr("autocomplete","off");
var F=G.attr("data-max")||10,I=G.attr("data-alignment")||"left",H=G.attr("data-dropdown-target"),E=null;
if(H){E=D(H)
}else{E=D("<div></div>");
G.after(E)
}E.addClass("aui-dd-parent autocomplete");
G.quicksearch(AJS.REST.getBaseUrl()+"search/user.json",function(){G.trigger("open.autocomplete-sharepage")
},{makeParams:function(J){return{"max-results":F,query:J.replace("{|}","")}
},dropdownPlacement:function(J){E.append(J)
},makeRestMatrixFromData:B,addDropdownData:function(K){var J=D.trim(G.val());
if(A.test(J)){K.push([{name:J,email:J,href:"#",icon:AJS.Confluence.getContextPath()+"/download/resources/com.atlassian.confluence.plugins.share-page:mail-page-resources/images/envelope.png"}])
}if(!K.length){var L=G.attr("data-none-message");
if(L){K.push([{name:L,className:"no-results",href:"#"}])
}}return K
},ajsDropDownOptions:{alignment:I,displayHandler:function(J){if(J.restObj&&J.restObj.username){return J.name+" ("+J.restObj.username+")"
}return J.name
},selectionHandler:function(L,K){if(K.find(".search-for").length){G.trigger("selected.autocomplete-sharepage",{searchFor:G.val()});
return 
}if(K.find(".no-results").length){this.hide();
L.preventDefault();
return 
}var J=D("span:eq(0)",K).data("properties");
if(!J.email){J=J.restObj
}G.trigger("selected.autocomplete-sharepage",{content:J});
this.hide();
L.preventDefault()
}}})
})
};
(function(A){jQuery.fn.extend({elastic:function(){var B=["paddingTop","paddingRight","paddingBottom","paddingLeft","fontSize","lineHeight","fontFamily","width","fontWeight","border-top-width","border-right-width","border-bottom-width","border-left-width","borderTopStyle","borderTopColor","borderRightStyle","borderRightColor","borderBottomStyle","borderBottomColor","borderLeftStyle","borderLeftColor"];
return this.each(function(){if(this.type!=="textarea"){return false
}var G=jQuery(this),C=jQuery("<div />").css({position:"absolute",display:"none","word-wrap":"break-word","white-space":"pre-wrap"}),I=parseInt(G.css("line-height"),10)||parseInt(G.css("font-size"),"10"),K=parseInt(G.css("height"),10)||I*3,J=parseInt(G.css("max-height"),10)||Number.MAX_VALUE,D=0;
if(J<0){J=Number.MAX_VALUE
}C.appendTo(G.parent());
var F=B.length;
while(F--){C.css(B[F].toString(),G.css(B[F].toString()))
}function H(){var M=Math.floor(parseInt(G.width(),10));
if(C.width()!==M){C.css({width:M+"px"});
E(true)
}}function L(M,O){var N=Math.floor(parseInt(M,10));
if(G.height()!==N){G.css({height:N+"px",overflow:O})
}}function E(P){var O=G.val().replace(/&/g,"&amp;").replace(/ {2}/g,"&nbsp;").replace(/<|>/g,"&gt;").replace(/\n/g,"<br />");
var M=C.html().replace(/<br>/ig,"<br />");
if(P||O+"&nbsp;"!==M){C.html(O+"&nbsp;");
if(Math.abs(C.height()+I-G.height())>3){var N=C.height()+I;
if(N>=J){L(J,"auto")
}else{if(N<=K){L(K,"hidden")
}else{L(N,"hidden")
}}}}}G.css({overflow:"hidden"});
G.bind("keyup change cut paste",function(){E()
});
A(window).bind("resize",H);
G.bind("resize",H);
G.bind("update",E);
G.bind("input paste",function(M){setTimeout(E,250)
});
E()
})
}})
})(AJS.$);
(function(E){var D,B={hideCallback:A,width:250,hideDelay:3600000,calculatePositions:function(G,N,V,R){var O;
var X;
var T;
var K=-7;
var L;
var P;
var W=N.target.offset();
var F=N.target.outerWidth();
var I=W.left+F/2;
var S=(window.pageYOffset||document.documentElement.scrollTop)+E(window).height();
var J=10;
T=W.top+N.target.outerHeight()+R.offsetY;
O=W.left+R.offsetX;
var M=W.top>G.height();
var H=(T+G.height())<S;
P=(!H&&M)||(R.onTop&&M);
var Q=E(window).width()-(O+R.width+J);
if(P){T=W.top-G.height()-8;
var U=R.displayShadow?(AJS.$.browser.msie?10:9):0;
K=G.height()-U
}L=I-O+R.arrowOffsetX;
if(R.isRelativeToMouse){if(Q<0){X=J;
O="auto";
L=V.x-(E(window).width()-R.width)
}else{O=V.x-20;
X="auto";
L=V.x-O
}}else{if(Q<0){X=J;
O="auto";
L=I-(E(window).width()-G.outerWidth())
}else{if(R.width<=F/2){L=R.width/2;
O=I-R.width/2
}}}return{displayAbove:P,popupCss:{left:O,right:X,top:T},arrowCss:{position:"absolute",left:L,right:"auto",top:K}}
}};
var A=function(){E(".dashboard-actions .explanation").hide()
};
var C=function(I,G,H){if(I.find("input").length){H();
return 
}I.append(AJS.template.load("share-content-popup").fill());
AJS.Confluence.SharePage.autocompleteUser();
var J=function(L){D.hide();
if(L){setTimeout(function(){I.empty()
},300)
}return false
};
E(document).keyup(function(L){if(L.keyCode==27){J(true);
E(document).unbind("keyup",arguments.callee);
return false
}return true
});
I.find(".close-dialog").click(function(){J(true)
});
I.find("#note").elastic();
I.find("form").submit(function(){var P=[];
I.find(".recipients li").each(function(Q,R){P.push(E(R).attr("data-username"))
});
if(P.length<=0){return false
}E("button,input,textarea",this).attr("disabled","disabled");
I.find(".progress-messages-icon").removeClass("error");
I.find(".progress-messages").text("Sending");
I.find(".progress-messages").attr("title","Sending");
var M=Raphael.spinner(I.find(".progress-messages-icon")[0],7,"#666");
I.find(".progress-messages-icon").css("position","absolute").css("left","0").css("margin-top","3px");
I.find(".progress-messages").css("padding-left",I.find(".progress-messages-icon").innerWidth()+5);
var P=[];
I.find(".recipients li[data-username]").each(function(Q,R){P.push(E(R).attr("data-username"))
});
var O=[];
I.find(".recipients li[data-email]").each(function(Q,R){O.push(E(R).attr("data-email"))
});
var L=I.find("#note");
var N={users:P,emails:O,note:L.hasClass("placeholded")?"":L.val(),entityId:AJS.params.pageId};
E.ajax({type:"POST",contentType:"application/json; charset=utf-8",url:AJS.Confluence.getContextPath()+"/rest/share-page/latest/share",data:JSON.stringify(N),dataType:"text",success:function(){setTimeout(function(){M();
I.find(".progress-messages-icon").css("width","16px");
I.find(".progress-messages-icon").css("height","16px");
I.find(".progress-messages-icon").addClass("done");
I.find(".progress-messages").text("Sent");
I.find(".progress-messages").attr("title","Sent");
setTimeout(function(){J(true)
},1000)
},500)
},error:function(R,Q){M();
I.find(".progress-messages-icon").css("width","16px");
I.find(".progress-messages-icon").css("height","16px");
I.find(".progress-messages-icon").addClass("error");
I.find(".progress-messages").text("Error while sending");
I.find(".progress-messages").attr("title","Error while sending");
E("button,input,textarea",I).removeAttr("disabled")
}});
return false
});
var K=I.find("#users");
var F=I.find("input.submit");
K.bind("selected.autocomplete-sharepage",function(M,L){var N=function(P,Q){var S=I.find(".recipients"),R,O;
R="li[data-"+P+'="'+Q.content[P]+'"]';
if(S.find(R).length>0){S.find(R).hide()
}else{S.append(AJS.template.load("share-content-popup-recipient-"+P).fill(Q.content))
}O=S.find(R);
O.find(".remove-recipient").click(function(){O.remove();
if(S.find("li").length==0){F.attr("disabled","true")
}D.refresh();
K.focus();
return false
});
O.fadeIn(200)
};
if(L.content.email){N("email",L)
}else{N("username",L)
}D.refresh();
F.removeAttr("disabled");
K.val("");
return false
});
K.bind("open.autocomplete-sharepage",function(M,L){if(E("a:not(.no-results)",AJS.dropDown.current.links).length>0){AJS.dropDown.current.moveDown()
}});
K.keypress(function(L){if(L.keyCode==13){return false
}return true
});
E(document).bind("showLayer",function(N,M,L){if(M=="inlineDialog"&&L.popup==D){L.popup.find("#users").focus()
}});
E("#shareContentLink").parents().filter(function(){return this.scrollTop>0
}).scrollTop(0);
H()
};
AJS.toInit(function(F){D=AJS.InlineDialog(F("#shareContentLink"),"shareContentPopup",C,B)
})
})(AJS.$);
} catch (err) {
    if (console && console.log && console.error) {
        console.log("Error running batched script.");
        console.error(err);
    }
}


try {
AJS.toInit(function ($) {
    $("#action-view-source-link").click(function (e) {
        window.open(this.href, (this.id + "-popupwindow").replace(/-/g, "_"), "width=800, height=600, scrollbars, resizable");
            e.preventDefault();
            return false;
        });
});
} catch (err) {
    if (console && console.log && console.error) {
        console.log("Error running batched script.");
        console.error(err);
    }
}


try {
AJS.toInit(function ($) {
    $(".view-storage-link, .view-storage-link a").click(function (e) {
        window.open(this.href, (this.id + "-popupwindow").replace(/-/g, "_"), "width=800, height=600, scrollbars, resizable");
            e.preventDefault();
            return false;
        });
});

} catch (err) {
    if (console && console.log && console.error) {
        console.log("Error running batched script.");
        console.error(err);
    }
}


try {
AJS.toInit(function($) {
    function autoSize(embeds, attempt) {
        var retry;

        if(attempt >= 20) { // 2 sec
            AJS.log('unable to auto size flash - took too long to load');
            return;
        }

        retry = $([]);

        embeds.each(function() {
            var $e = $(this);
            var h, w;
            if(this.GetVariable) {
                // Only set width/height is not already set
                if(!$e.attr("height")) {
                    h = this.GetVariable("height");
                    if(h) {
                        $e.height(h);
                    } else {
                        retry = retry.add($e);
                        return;
                    }
                }
                if(!$e.attr("width")) {
                    w = this.GetVariable("width");
                    if(w) {
                        $e.width(w);
                    } else {
                        retry = retry.add($e);
                        return;
                    }
                }
            }
        });

        if(retry.length) {
            setTimeout(function() {
                autoSize(retry, attempt + 1);
            }, 100);
        }
    }

    autoSize($('embed[type="application/x-shockwave-flash"]'), 0);

    // For preview
    $(window).bind("render-content-loaded", function(e, body) {
        autoSize($('embed[type="application/x-shockwave-flash"]', body), 0);
    });
});

} catch (err) {
    if (console && console.log && console.error) {
        console.log("Error running batched script.");
        console.error(err);
    }
}


