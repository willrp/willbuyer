//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import ImageGallery from "react-image-gallery";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const thumbnailClass = css({
    "&&&&&.active": {
        borderColor: "deepskyblue"
    },
    "&&&&:hover": {
        borderColor: "lightskyblue"
    }
})

//COMPONENT=================================================================
function Gallery({ images }) {
    function render() {
        const items = images.map(
            (item) => {
                return {
                    original: item,
                    thumbnail: item.replace("wid=500", "wid=150"),
                    thumbnailClass: thumbnailClass
                }
            }
        );

        return (
            <ImageGallery
                infinite
                autoPlay
                items={items}
                showThumbnails
                thumbnailPosition="bottom"
                showFullscreenButton={false}
            />
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default Gallery;