//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { useParams } from "react-router-dom";

//IMPORT INTERNAL COMPONENTS================================================
import ProductsContent from "components/products-content";

//COMPONENT=================================================================
function Brand() {
    const { brand } = useParams();
    const preffix = "/api/store/find";
    const type = "brand";
    const arg = brand;

    return <ProductsContent urlobj={{preffix, type, arg}} />
}

//EXPORT COMPONENT==========================================================
export default Brand;