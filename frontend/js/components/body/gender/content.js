//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState, useContext, useEffect } from "react";
import { Header } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ContentLoading from "components/util/content-loading";
import NotFound from "components/util/not-found";
import DiscountsSlider from "./discounts-slider";
import SessionGrid from "./session-grid";

//IMPORT CONTEXTS===========================================================
import { SidebarContext } from "contexts/sidebar-context";

//IMPORT HOOKS==============================================================
import useRequestData from "hooks/request-data";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const headerClass = css({
    "&&&&&": {
        marginTop: "0.5em"
    }
})

//COMPONENT=================================================================
function Content({ gender }) {
    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);
    const { updateItems } = useContext(SidebarContext);

    useEffect(() => {
        setRequest({
            url: `/api/store/gender/${gender}`,
            method: "post",
            responseType: "json",
            data: {
                amount: 24
            }
        })
    }, [gender])

    useEffect(() => {
        const { status, data, error } = requestData;
        if(status === 200 && data !== null){
            const { sessions, brands, kinds } = data;
            updateItems(sessions, brands, kinds);
        }
        else if(status >= 400 && error !== null){
            throw {status, error};
        }
    }, [requestData])

    function render() {
        const { data, status, loading } = requestData;
        if(loading === true) {
            return <ContentLoading />
        }
        else if(status === 204 || data === null) {
            return <NotFound />
        }
        else{
            const { discounts, sessions } = data;
            return(
                <Fragment>
                    <Header className={headerClass} as="h1" textAlign="center" dividing>Super Discounts</Header>
                    <DiscountsSlider discounts={discounts} />
                    <Header className={headerClass} as="h1" textAlign="center" dividing>Sessions</Header>
                    <SessionGrid sessions={sessions} />
                </Fragment>
            )
        }
    }
    
    return render()
}

//EXPORT COMPONENT==========================================================
export default Content;