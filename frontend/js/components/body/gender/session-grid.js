//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Link } from "react-router-dom";
import { Image, Grid, Card } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ResponsiveGrid from "components/util/responsive-grid";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const gridClass = css({
    "&&&&&": {
        margin: "0"
    }
})

const columnClass = css({
    "&&&&&": {
        padding: "0.5em",
        display: "flex"
    },
    "&&&&&>.card": {
        flexGrow: 1,
        margin: 0
    }
})

//COMPONENT=================================================================
function SessionGrid({ sessions }) {
    function renderSessions() {
        return sessions.map(
            (item) => {
                const { image, name, total, id } = item;
                return (
                    <Grid.Column key={id} className={columnClass}>
                        <Card as={Link} to={`/session/${id}`} centered>
                            <Image src={image} wrapped ui={false} />
                            <Card.Content>
                                <Card.Header textAlign="center">{name}</Card.Header>
                                <Card.Meta textAlign="center">{total} products</Card.Meta>
                            </Card.Content>
                        </Card>
                    </Grid.Column>
                )
            }
        )
    }

    function render() {
        return (
            <ResponsiveGrid
                className={gridClass}
                largescreen={5}
                computer={4}
                tablet={3}
                mobile={2}
            >
                {renderSessions()}
            </ResponsiveGrid>
        )
    }
    
    return render()
}

//EXPORT COMPONENT==========================================================
export default SessionGrid;