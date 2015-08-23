try {
AJS.$(document).bind(AppLinks.Event.READY,function(){(function(A){AppLinks.OAuthCallback=function(){};
AppLinks.OAuthCallback.prototype.success=function(){this.aouthWindow.close();
this.onSuccess()
};
AppLinks.OAuthCallback.prototype.failure=function(){this.aouthWindow.close();
this.onFailure()
};
AppLinks.OAuthCallback.prototype.show=function(B,D,C){this.onSuccess=D;
this.onFailure=C;
this.aouthWindow=window.open(B,"com_atlassian_applinks_authentication")
};
oauthCallback=new AppLinks.OAuthCallback();
AppLinks.authenticateRemoteCredentials=function(B,D,C){A(".applinks-error").remove();
oauthCallback.show(B,D,C)
}
})(AJS.$)
});
} catch (err) {
    if (console && console.log && console.error) {
        console.log("Error running batched script.");
        console.error(err);
    }
}


