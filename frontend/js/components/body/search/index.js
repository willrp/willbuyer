//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { useParams } from "react-router-dom";

//IMPORT INTERNAL COMPONENTS================================================
import ProductsContent from "components/products-content";

//COMPONENT=================================================================
function Search() {
    const { query } = useParams();
    const preffix = "/api/store/find";
    const type = "search";
    const arg = query;

    return <ProductsContent urlobj={{preffix, type, arg}} />
}

//EXPORT COMPONENT==========================================================
export default Search;