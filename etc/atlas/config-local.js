define([], function () {
        var configLocal = {}
        configLocal.api = {
                name: 'OHDSI',
                url: '${WEBAPI_URL}',
        };
        configLocal.cohortComparisonResultsEnabled = false;
        configLocal.userAuthenticationEnabled = true;
        configLocal.plpResultsEnabled = false;
        configLocal.authProviders = [{
                "name": "Keycloak",
                "url": "user/login/openid",
                "ajax": false,
                "icon": "fa fa-openid",
        }];
        return configLocal;
});
