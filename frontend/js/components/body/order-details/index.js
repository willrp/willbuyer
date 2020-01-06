//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Header } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ContentLoading from "components/util/content-loading";
import NotFound from "components/util/not-found";
import OrderInfo from "./order-info";
import OrderItems from "./order-items";

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
    const { orderid } = useParams();
    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);

    useEffect(() => {
        setRequest({
            url: `/api/order/${orderid}`,
            method: "get",
            responseType: "json"
        })
    }, [orderid])

    function render() {
        const { data, status, loading } = requestData;
        if(loading === true) {
            return <ContentLoading />
        }
        else if(status === 404) {
            return <NotFound />
        }
        else {
            const { product_types, items_amount, total, updated_at, products } = data;
            return (
                <Fragment>
                    <Header className={headerClass} as="h1" textAlign="center" dividing>Order Details</Header>
                    <OrderInfo {...{ product_types, items_amount, total, updated_at }} />
                    <OrderItems items={products} />
                </Fragment>
            )
        }
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default Orders;