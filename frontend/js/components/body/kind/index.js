//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { withRouter } from "react-router-dom";

//IMPORT INTERNAL COMPONENTS================================================
import ProductsContent from "components/products-content";

//COMPONENT=================================================================
function Kind({ match }) {
    const { kind } = match.params;
    const preffix = "/api/store/find";
    const type = "kind";
    const arg = kind;

    return <ProductsContent urlobj={{preffix, type, arg}} />
}

//EXPORT COMPONENT==========================================================
export default withRouter(Kind);