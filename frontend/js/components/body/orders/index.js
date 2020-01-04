//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState, useEffect } from "react";
import { Header, Message, Icon } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ContentLoading from "components/util/content-loading";
import OrdersContent from "./orders-content";

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
function Orders() {
    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);
    const pageSize = 12;

    useEffect(() => {
        setRequest({
            url: "/api/order/user",
            method: "post",
            responseType: "json",
            data: {
                page: 1,
                page_size: pageSize
            }
        })
    }, [])

    useEffect(() => {
        const { status, error } = requestData;
        if(status >= 400 && error !== null){
            throw {status, error};
        }
    }, [requestData])

    function renderEmptyOrders() {
        return(
            <Message icon info className={headerClass}>
                <Icon name="shopping basket" />
                <Message.Content>
                    <Message.Header>Information</Message.Header>
                    You still did not place any orders.
                </Message.Content>
            </Message>
        )
    }
    
    function render() {
        const { data, status, loading } = requestData;
        if(loading === true) {
            return <ContentLoading />
        }
        else {
            return ( 
                <Fragment>
                    <Header className={headerClass} as="h1" textAlign="center" dividing>Orders</Header>
                    {(status === 204 || data === null) ? renderEmptyOrders() : <OrdersContent {...data} pageSize={pageSize} />}
                </Fragment>
            )
        }
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default Orders;