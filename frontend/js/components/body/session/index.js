//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { useParams } from "react-router-dom";

//IMPORT INTERNAL COMPONENTS================================================
import ProductsContent from "components/products-content";

//COMPONENT=================================================================
function Session() {
    const { sessionid } = useParams();
    const preffix = "/api/store";
    const type = "session";
    const arg = sessionid;

    return <ProductsContent urlobj={{preffix, type, arg}} />
}

//EXPORT COMPONENT==========================================================
export default Session;