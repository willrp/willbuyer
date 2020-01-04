//IMPORT EXTERNAL COMPONENTS================================================
import React, {lazy, memo, Suspense} from "react";
import { Route, Switch, Redirect } from "react-router-dom";
import { Container } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import LoadableLoading from "components/util/loadable-loading";
import PrivateRoute from "components/util/private-route";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const containerClass = css({
    "&&&&&": {
        paddingBottom: "1em"
    }
})

//COMPONENT=================================================================
function Body() {
    const Home = lazy(() => import("./home"));
    const Gender = lazy(() => import("./gender"));
    const Session = lazy(() => import("./session"));
    const Brand = lazy(() => import("./brand"));
    const Kind = lazy(() => import("./kind"));
    const Search = lazy(() => import("./search"));
    const Product = lazy(() => import("./product"));
    const Cart = lazy(() => import("./cart"));
    const Orders = lazy(() => import("./orders"));
    const OrderDetails = lazy(() => import("./order-details"));
    const Login = lazy(() => import("./login"));
    const NotFound = lazy(() => import("components/util/not-found"));

    return (
        <Container className={containerClass}>
            <Suspense fallback={<LoadableLoading />}>
                <Switch>
                    <Route exact path="/" component={Home} />
                    <Route exact path="/outlet/:gender" component={Gender} />
                    <Route exact path="/session/:sessionid" component={Session} />
                    <Route exact path="/brand/:brand" component={Brand} />
                    <Route exact path="/kind/:kind" component={Kind} />
                    <Route exact path="/search/:query" component={Search} />
                    <Route exact path="/product/:productid" component={Product} />
                    <Route exact path="/cart" component={Cart} />
                    <PrivateRoute exact path="/orders" component={Orders} />
                    <PrivateRoute exact path="/order/:orderid" component={OrderDetails} />
                    <Route exact path="/404" component={NotFound} />
                    <Route exact path="/login" component={Login} />
                    <Redirect to="/404" />
                </Switch>
            </Suspense>
        </Container>
    )
}

//EXPORT COMPONENT==========================================================
export default memo(Body);