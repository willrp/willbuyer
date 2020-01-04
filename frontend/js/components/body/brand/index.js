//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { withRouter } from "react-router-dom";

//IMPORT INTERNAL COMPONENTS================================================
import ProductsContent from "components/products-content";

//COMPONENT=================================================================
function Brand({ match }) {
    const { brand } = match.params;
    const preffix = "/api/store/find";
    const type = "brand";
    const arg = brand;

    return <ProductsContent urlobj={{preffix, type, arg}} />
}

//EXPORT COMPONENT==========================================================
export default withRouter(Brand);