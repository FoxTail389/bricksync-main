<script lang="ts">
  import { Stage, Layer, Image, Circle, Line } from "svelte-konva";
  let state = 0;
  let imgwidth: any = null;
  let imgheight: any = null;
  let width = window.innerWidth;
  let height: any = null;
  //https://konvajs.org/docs/svelte/index.html
  //
  let y2: number = 0;
  let md:any;
  let mn:any;
  let perpLine;
  let perpLineRev;
  let cir1_config: any;
  let cir2_config: any;
  let cir3_config:any;
  let image: any = null;
  const img = document.createElement("img");
  img.className = "w-screen";
  img.src = "News Recording.png";
  img.onload = () => {
    imgheight = img.height;
    imgwidth = img.width;
    image = img;
    image.height = Math.round(img.height / (img.width / width));
    image.width = width;
    height = image.height;
  };
  let n: any;
  function getMousePosition(event: any) {
    let rect = event.target.getBoundingClientRect();
    const percent = width / imgwidth;
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    n = [Math.round(x / percent), Math.round(y / percent), x, y];
    if (state == 2) {
    }
    return n;
  }
  // @ts-ignore

  function click(event: any) {
    let a = getMousePosition(event);
    if (state == 0) {
      cir1_config = {
        x: a[2],
        y: a[3],
        radius: 5,
        fill: "green",
      };
      state += 1;
    } else if (state == 1) {
       mn = -(a[2] - cir1_config.x);
       md = a[3] - cir1_config.y;
      if (md == 0) {
        perpLine = (x: number) => mn;
        y2 = 1;
      } else if (mn == 0) {
        perpLine = (y: number) => a[3];
        y2 = 2;
      } else {
        perpLine = (y: number) => (mn / md) * (y - a[2]) + a[3];
        perpLineRev = (x: number) => (md / mn) * (x - a[3]) + a[2];
      }
      cir2_config = {
        x: a[2],
        y: a[3],
        radius: 5,
        fill: "green",
      };
      cir3_config = {
        x: (cir1_config.x + cir2_config.x) / 2,
        y: (cir1_config.y + cir2_config.y) / 2,
        radius: 5,
        fill: "green",
      };
      state += 1;
    }
    console.log(getMousePosition(event));
  }
  function cancel() {
    state = 0;
    cir1_config = null;
    cir2_config=null
    
  }
</script>

<button class="w-full" on:click={click} on:mousemove={getMousePosition}>
  <Stage config={{ width: width, height: height }}>
    <Layer>
      {#if cir1_config}
        <Circle config={cir1_config} />
      {/if}
      {#if cir2_config}
        <Circle config={cir2_config} />
      {/if}
      {#if state == 1}
        <Line
          config={{
            points: [cir1_config.x, cir1_config.y, n[2], n[3]],
            stroke: "green",
            strokeWidth: 2,
          }}
        />
      {:else if state == 2}
        <Circle config={cir3_config} />
        <Line
          config={{
            points: [
              cir1_config.x,
              cir1_config.y,
              cir2_config.x,
              cir2_config.y,
            ],
            stroke: "green",
            strokeWidth: 2,
          }}
        />
      {/if}
      <Image config={{ image }} />
    </Layer>
  </Stage>
</button>
<button on:click={cancel}>Cancel</button>
<!--<canvas id="myCanvas" on:mousemove={getMousePosition} style="background:url('News Recording.png')"-->
