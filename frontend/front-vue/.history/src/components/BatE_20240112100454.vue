
<template>
    <div>
        <h2>Bat E</h2>
        <svg id="svg3" inkscape:version="1.3.2 (091e20ef0f, 2023-11-25, custom)" sodipodi:docname="batiment-e.svg" version="1.1" viewBox="0 0 2141.3 1064" xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">
            <g id="rdc" class="changeColor" transform="matrix(.99999 0 0 .99999 -14.992 -18.924)">
                <title id="title1">Rez-de-chaussée</title>
                <path id="path34412" d="m349.07 675.08 0.0151 132.11 256.76 143.59-1.6675-163.69z" />
                <path id="path34414" d="m1815.8 659.75 0.2858-147-1210.9 274.71 0.83408 163.6z" />
                <path id="path35587" d="m168.81 701.55 114.21-38.15-207.36 95.093c-22.534 17.51-27.533 52.444-2.2531 72.43 68.164 44.517 146.17 39.822 224.87 31.65l238.23 150.43c49.327 20.628 74.178 22.023 156.25-0.5427l1101-296.28c37.922 28.901 82.743 35.139 197.36 29.553 58.443-10.344 119.19-19.227 134.99-56.634 2.2596-25.044-18.158-44.482-64.851-57.426l-18.991-49.08-228.94 77.724-1207.9 291.06z" />
            </g>
            <g id="et1" class="changeColor" transform="matrix(.99999 0 0 .99999 -14.992 -18.924)">
                <title id="title2">Premier étage</title>
                <path id="path33561" d="m170.23 475.31-0.2364 120.28 433.99 191.78-1.4349-157.72z" />
                <path id="path33662" d="m1815.4 364.49 0.4121 147.76-1211.4 275.25-1.1834-158.34z" />
            </g>
            <g id="et2" class="changeColor" transform="matrix(.99999 0 0 .99999 -14.992 -18.924)">
                <title id="title3">Deuxième étage</title>
                <path id="path4789" d="m102.32 325.03 469.25 134.43 30.168-11.198 0.37064 180.69-501.24-167.16z" />
                <path id="path9213" d="m2063 194.11-0.6412 116-1459.7 319.13-1.2471-180.76z" />
                <path id="path4564" d="m686.19 190.74 1069-131.92 332.91 65.836 32.805 60.248-1532.6 287.24" />
                <path id="path4786" d="m686.19 190.23-652.52 100.96-8.3446 23.301 564.72 157.55z" />
            </g>
            <g id="cylindre" transform="matrix(.99999 0 0 .99999 337.14 27.353)">
                <path id="path5191" d="m1462.8 235.73c9.2665-16.962 48.981-27.606 127.28-28.795 102.02 1.8549 129.92 16.268 132.49 30.344-20.134 24.604-83.038 24.054-133.98 25.62-51.116-1.5698-105.68-2.0954-125.79-27.17z"/>
                <path id="path6309" d="m1722.6 237.28-0.3909 383.93c-14.143 21.494-86.223 24.819-130.14 25.69-46.133-0.45692-123.51-5.2424-127.25-32.37l-1.9903-378.8c27.501 28.161 79.191 24.292 125.79 27.17 58.508-1.0565 115.79-2.7777 133.98-25.62"/>
            </g>
            <g id="cylindre2" transform="matrix(.99999 0 0 .99999 -1388.5 139.91)">
                <path id="path3" d="m1462.8 235.73c-4.8278-18.716 21.564-57.424 97.215-37.209l164.15 43.861c-20.134 24.604-84.633 18.952-135.57 20.519-51.116-1.5698-117.76 3.9538-125.79-27.17z"/>
                <path id="path4" d="m1722.8 243.5-0.5687 404.03c-14.143 21.494-86.223 24.819-130.14 25.69-46.133-0.45692-123.51-5.2424-127.25-32.37l-1.9903-405.13c30.519 23.13 56.554 28.316 125.79 27.17 58.508-1.0565 92.646-1.7612 133.98-19.574"/>
            </g>
        </svg>
        <BatBRdc v-if="showRdc" />
        <BatBetage1 v-else-if="showEt1" />
        <BatBetage2 v-else-if="showEt2" />
    </div>
  </template>
  
  <script>
  import BatERdc from './BatERdc.vue';
  import BatEetage1 from './BatEetage1.vue';
  import BatEetage2 from './BatEetage2.vue';
  export default {
        data() {
            return {
            showRdc: false,
            showEt1: false,
            showEt2: false,
            };
        },
        methods: {
            
            displayBatERdc() {
                this.showRdc = true;
                this.showEt1 = false;
                this.showEt2 = false;
                },
            displayBatEEt1() {
                this.showRdc = false;
                this.showEt1 = true;
                this.showEt2 = false;
                },
            displayBatEEt2() {
                this.showRdc = false;
                this.showEt1 = false;
                this.showEt2 = true;
                },
            },
        components: {
            BatBRdc,
            BatBetage1,
            BatBetage2
        },
    }
  </script>

<style>
svg {
    border: dashed black 1px;
}
g {
    fill:rgb(183, 232, 247);
    stroke:rgb(0, 26, 255);
    
    /* stroke:rgb(0, 0, 0);
    fill: rgb(248, 183, 43); */
    
    fill-opacity:1;
    stroke-width:1px;
    stroke-linecap:round;
    stroke-linejoin:round;
    stroke-opacity:1;
    
    transition: fill 1.2s, stroke 1s
}
g.changeColor:hover {
    stroke:rgb(56, 0, 102);
    fill: rgb(247, 156, 239);
    
    /* stroke:rgb(255, 193, 183);
    fill: rgb(233, 8, 0); */
}



</style>
  