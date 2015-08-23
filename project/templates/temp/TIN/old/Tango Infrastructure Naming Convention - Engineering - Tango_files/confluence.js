try {
AJS.JiraIssues={Remote:{}};
var appLinksI18n={entries:{}};
jQuery(document).ready(function(){AJS.JiraIssues=jQuery.extend(AJS.JiraIssues||{},{bindOAuthLink:function(D,G){var F={onSuccess:function(){G()
},onFailure:function(){}};
var E=D.attr("href");
D.click(function(H){AppLinks.authenticateRemoteCredentials(E,F.onSuccess,F.onFailure);
H.preventDefault()
})
},getOAuthRealm:function(G){var E=G.getResponseHeader("WWW-Authenticate")||"";
var D=/OAuth realm\=\"([^\"]+)\"/;
var F=D.exec(E);
if(F){return F[1]
}else{return null
}}});
jQuery("a.static-oauth-init").each(function(){AJS.JiraIssues.bindOAuthLink(jQuery(this),function(){window.location.reload()
})
});
var B=function(J){var F=AJS.JiraIssues.Remote[J];
var I="";
for(var H=0;
H<F.length;
H++){I=I+(F[H].key+(H<F.length-1?",":""))
}var E=function(M){var K="issuekey in ("+M+")";
var N="/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?jqlQuery="+encodeURIComponent(K);
var L=contextPath+"/plugins/servlet/issue-retriever?appId="+J+"&url="+encodeURIComponent(N)+"&columns=summary&columns=type&columns=resolution&columns=status";
return L
};
var G=function(L){var K=AJS.$("item",L);
K.each(function(){var V=AJS.$("link",this).text();
var W=AJS.$("key",this).text();
var S=AJS.$("summary",this).text();
var T=AJS.$("type",this);
var N=AJS.$("resolution",this);
var X=N.attr("id")!="-1";
var P=AJS.$("status",this);
var O=AJS.$(".unknown-jira-issue."+W);
for(var Q=0;
Q<O.length;
Q++){var U=AJS.$("<a style=\"background-image: url('"+T.attr("iconUrl")+'\')" href="'+V+'"></a>');
U.text(W);
var M=AJS.$('<span class="jira-status"></span>');
M.text(P.text().toUpperCase());
var R=AJS.$('<span class="jira-issue'+(X?" resolved":"")+'" ></span>');
R.append(U);
R.append(document.createTextNode(" - "+S+" - "));
R.append(M);
AJS.$(O[Q]).replaceWith(R)
}})
};
var D=E(I);
AJS.$.ajax({url:D,success:G,error:function(M){if(M.status==401){var L=AJS.JiraIssues.getOAuthRealm(M);
if(L){var K={};
AJS.$(F).each(function(){if(!K[this.key]){K[this.key]=true;
var N=AJS.$('<span class="oauth-msg"> - <a class="oauth-init" href="'+L+'">'+"Authenticate"+"</a> "+"to see issue details"+"</span>");
AJS.$(".unknown-jira-issue."+this.key).addClass("single-issue-oauth").append(N)
}});
AJS.JiraIssues.bindOAuthLink(AJS.$(".single-issue-oauth a.oauth-init"),function(){window.location.reload()
})
}}else{if(M.status==400&&F.length>1){AJS.$(F).each(function(){var N=this.key;
var O=E(N);
AJS.$.ajax({url:O,success:G,error:function(Q){var P=AJS.$(".unknown-jira-issue."+N);
P.removeClass("single-issue-oauth");
AJS.$(".oauth-msg",P).remove();
P.addClass("jira-error")
}})
})
}}}})
};
var A={};
AJS.$(".unknown-jira-issue").each(function(F,G){var E=AJS.$(G);
var H=E.attr("data-app-link");
var D=E.attr("data-key");
AJS.JiraIssues.Remote[H]=AJS.JiraIssues.Remote[H]||[];
AJS.JiraIssues.Remote[H].push({key:D})
});
for(var C in AJS.JiraIssues.Remote){B(C)
}});
} catch (err) {
    if (console && console.log && console.error) {
        console.log("Error running batched script.");
        console.error(err);
    }
}


