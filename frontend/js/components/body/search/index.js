//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { withRouter } from "react-router-dom";

//IMPORT INTERNAL COMPONENTS================================================
import ProductsContent from "components/products-content";

//COMPONENT=================================================================
function Search({ match }) {
    const { query } = match.params;
    const preffix = "/api/store/find";
    const type = "search";
    const arg = query;

    return <ProductsContent urlobj={{preffix, type, arg}} />
}

//EXPORT COMPONENT==========================================================
export default withRouter(Search);