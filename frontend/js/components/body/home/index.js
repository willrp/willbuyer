//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { Message, Grid, Image } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import imgmen from "img/men.jpg";
import imgwomen from "img/women.jpg";

//IMPORT CONTEXTS===========================================================
import { SidebarContext } from "contexts/sidebar-context";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const messageClass = css({
    "&&&&": {
        marginBottom: "2px"
    }
})

const gridClass = css({
    "&&&&&": {
        margin: "0"
    },
    "&&&&& .column": {
        paddingTop: "0",
        paddingBottom: "0"
    }
})

const imgClass = css({
    "&&&&": {
        width: "49%",
        height: "auto",
        padding: "1px"
    }
})

//COMPONENT=================================================================
function Home() {
    const { updateItems } = useContext(SidebarContext);

    useEffect(() => {
        updateItems([], [], []);
    }, [])

    return (
        <Fragment>
            <Message className={messageClass}>
                <Message.Header>Disclaimer</Message.Header>
                <p>
                    This Web application is for demonstration purposes only. You cannot do real shopping here.
                    Thank you for understanding. <br /> Author: Will Roger Pereira
                </p>
            </Message>
            <Grid className={gridClass}>
                <Grid.Row columns={2}>
                    <Grid.Column 
                        className={imgClass}
                        as={Link}
                        to="/outlet/men"
                    >
                        <Image src={imgmen} />
                    </Grid.Column>
                    <Grid.Column
                        className={imgClass}
                        as={Link}
                        to="/outlet/women"
                    >
                        <Image src={imgwomen} />
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        </Fragment>
    )
}

//EXPORT COMPONENT==========================================================
export default Home;