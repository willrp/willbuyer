//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState, useContext, useEffect } from "react";
import { useLocation, useRouteMatch } from "react-router";
import { Redirect } from "react-router-dom";
import { Header } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ContentLoading from "components/util/content-loading";
import NotFound from "components/util/not-found";
import NoContent from "components/util/no-content";
import Products from "./products";

//IMPORT CONTEXTS===========================================================
import { SidebarContext } from "contexts/sidebar-context";

//IMPORT HOOKS==============================================================
import useRequestData from "hooks/request-data";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";
import { pick } from "lodash";
import queryString from "query-string";

//IMPORT INTERNAL FUNCTIONS=================================================
import validatePriceRange from "lib/validate-price-range";

//STYLE CLASSES DEFINITION==================================================
const headerClass = css({
    "&&&&&": {
        marginTop: "0.5em"
    }
})

//COMPONENT=================================================================
function ProductsContent({ urlobj }) {
    const { search } = useLocation();
    const match = useRouteMatch();
    const query = queryString.parse(search);
    const [pickedrange, setPickedRange] = useState(validatePriceRange(pick(query, ["min", "max"])));
    
    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);
    const { sidesessions, updateItems } = useContext(SidebarContext);
    const url = `${urlobj.preffix}/${urlobj.type}/${urlobj.arg}`;

    useEffect(() => {
        setRequest({
            url: url,
            method: "post",
            responseType: "json",
            data: {
                pricerange: pickedrange
            }
        })
    }, [url, pickedrange])

    useEffect(() => {
        const { data, status, error } = requestData;
        if(status === 200 && data !== null) {
            const { sessions, brands, kinds } = data;
            const sessiondata = (sessions === undefined) ? sidesessions : sessions;
            updateItems(sessiondata, brands, kinds);
        }
        else if(status === 204 && urlobj.type === "session") {
            setPickedRange(null);
        }
        else if((status === 400 || status >= 500) && error !== null) {
            throw {status, error};
        }
    }, [requestData])

    function makeName(sessions, arg) {
        if(sessions !== undefined) {
            return sessions.find((s) => s.id === arg).name;
        }
        else {
            return arg[0].toUpperCase() + arg.substring(1)
        }
    }

    function makeContentType(type) {
        if(type === "search") {
            return "Search query"
        }
        else {
            return type[0].toUpperCase() + type.substring(1)
        }
    }

    function render() {
        const { data, status, loading } = requestData;
        if(loading === true) {
            return <ContentLoading />
        }
        else if(status === 404) {
            return <NotFound />
        }
        else{
            if(status === 204 || data === null) {
                if(urlobj.type === "session") {
                    return <Redirect to={match.url} />
                }
                else if(urlobj.type === "search") {
                    return <NoContent message={`No products found for your search query ${urlobj.args}. Please try again.`} />
                }
                else {
                    return <NotFound />
                }
            }
            else {
                const { sessions, total, pricerange } = data;
                const normalizedRange = {min: Math.floor(pricerange.min), max: Math.ceil(pricerange.max)};
                return (
                    <Fragment>
                        <Header className={headerClass} as="h1" textAlign="center" dividing>
                            {makeName(sessions, urlobj.arg)}
                            <Header.Subheader>
                                {makeContentType(urlobj.type)}
                            </Header.Subheader>
                        </Header>
                        <Products url={url} pricerange={normalizedRange} total={total} />
                    </Fragment>
                )
            }
        }
    }
    
    return render()
}

//EXPORT COMPONENT==========================================================
export default ProductsContent;