//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { useParams } from "react-router-dom";

//IMPORT INTERNAL COMPONENTS================================================
import Content from "./content";

//COMPONENT=================================================================
function Gender() {
    const { gender } = useParams();

    return <Content gender={gender} />
}

//EXPORT COMPONENT==========================================================
export default Gender;