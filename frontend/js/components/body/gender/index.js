//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { withRouter } from "react-router-dom";

//IMPORT INTERNAL COMPONENTS================================================
import Content from "./content";

//COMPONENT=================================================================
function Gender(props) {
    const { gender } = props.match.params;

    return <Content gender={gender} />
}

//EXPORT COMPONENT==========================================================
export default withRouter(Gender);