//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment } from "react";
import { Link } from "react-router-dom";
import { Image, Header } from "semantic-ui-react";

//IMPORT INTERNAL ASSETS====================================================
import notfoundimg from "img/notfound.png";

//COMPONENT=================================================================
function NotFound() {
    return (
        <Fragment>
            <Image
                centered
                src={notfoundimg}
            />
            <span style={{textDecoration: "underline"}}>
                <Header as="h4" textAlign="center">
                    <Link to="/">Click here for a valid page.</Link>
                </Header>
            </span>
        </Fragment>
    )
}

//EXPORT COMPONENT==========================================================
export default NotFound;