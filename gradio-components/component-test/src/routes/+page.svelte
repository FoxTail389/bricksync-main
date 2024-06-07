<script lang="ts">
  import {
    Stage,
    Layer,
    Image,
    Circle,
    Line,
    Ellipse,
    Path,
  } from "svelte-konva";
  var Expression: any;
  var Equation: any;
  var Fraction: any;
  function equation() {
    // @ts-ignore
    Expression = algebra.Expression;
    // @ts-ignore
    Equation = algebra.Equation;
    // @ts-ignore
    Fraction = algebra.Fraction;
  }
  let state = 0;
  let imgwidth: any = null;
  let imgheight: any = null;
  let width = window.innerWidth;
  let height: any = null;
  //https://konvajs.org/docs/svelte/index.html
  //
  let cir1_config: any;
  let cir2_config: any;
  let cir3_config: any;
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
    let xpos = event.clientX - rect.left;
    let ypos = event.clientY - rect.top;
    n = [Math.round(xpos / percent), Math.round(ypos / percent), xpos, ypos];
    if (state == 2) {
      var x = new Expression("x");
      var y = new Expression("y");
      var mousex = new Fraction(xpos, 1);
      var mousey = new Fraction(ypos, 1);
      var mx = new Fraction(cir1_config["x"] + cir2_config["x"], 2); //new Expression("x1");
      var my = new Fraction(cir1_config["y"] + cir2_config["y"], 2); //new Expression("y1");
      var x2 = new Fraction(cir2_config["x"], 1); //new Expression("x2");
      var y2 = new Fraction(cir2_config["y"], 1); //new Expression("y2");
      var eq1 = new Equation(
        x.subtract(mx).multiply(x2.subtract(mx)),
        y.subtract(my).multiply(my.subtract(y2))
      );
      var mouseeq = new Equation(
        x.subtract(mousex).multiply(y2.subtract(my)),
        y.subtract(mousey).multiply(x2.subtract(mx))
      );
      var xeq;
      var yeq;
      try {
        var asy = eq1.solveFor("y");
        try {
          var asx = eq1.solveFor("x");
          var solveforx = new Equation(asy, mouseeq.solveFor("y"));
          xeq = solveforx.solveFor("x");
          var solvefory = new Equation(asx, xeq);
          yeq = solvefory.solveFor("y");
        } catch (err1) {
          yeq = asy;
          xeq = mouseeq.solveFor("x");
        }
      } catch (err) {
        xeq = eq1.solveFor("x");
        yeq = mouseeq.solveFor("y");
      }
      var pointx = Math.round(xeq["numer"] / xeq["denom"]);
      var pointy = Math.round(yeq["numer"] / yeq["denom"]);
      cir3_config.x = pointx;
      cir3_config.y = pointy;
      curveDir()
      console.log(
        Math.atan(
          (cir2_config.x - cir1_config.x) / (cir2_config.y - cir1_config.y)
        ) *
          (180 / Math.PI)
      );
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
        fill: "red",
      };
      state += 1;
    } else if (state == 1) {
      cir2_config = {
        x: a[2],
        y: a[3],
        radius: 5,
        fill: "yellow",
      };
      cir3_config = {
        x: (cir1_config.x + cir2_config.x) / 2,
        y: (cir1_config.y + cir2_config.y) / 2,
        radius: 5,
        fill: "green",
      };
      state += 1;
    } else if (state == 2) {
      state += 1;
    }
  }
  function cancel() {
    state = 0;
    cir1_config = null;
    cir2_config = null;
  }
  function curveDir(){
    let va:any = [cir1_config.x,cir1_config.y]
    let vb:any = [(cir1_config.x+cir2_config.x)/2,(cir1_config.y+cir2_config.y)/2]
    let vc:any = [cir3_config.x,cir3_config.y]
    let vu:any = [vb[0]-va[0],vb[1]-va[1]]
    let vv:any = [vc[0]-vb[0],vc[1]-vb[1]]
    let uxv = (vu[0]*vv[1])-(vu[1]*vv[0])
    if (uxv >= 0){
      return 0
    }else {
      return 1
    }
  }
</script>

<svelte:head>
  <script async src="algebra-0.2.6.min.js" on:load={equation}></script>
</svelte:head>
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
      {:else if state >= 2}
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
        <Path
          config={{
            x: cir1_config.x,
            y: cir1_config.y,
            stroke: "white",
            strokeWidth: 4,
            data: `M0 0 A ${Math.sqrt((cir1_config.x - cir2_config.x) ** 2 + (cir1_config.y - cir2_config.y) ** 2) / 2} ${Math.sqrt((cir3_config.x - (cir2_config.x + cir1_config.x) / 2) ** 2 + (cir3_config.y - (cir2_config.y + cir1_config.y) / 2) ** 2)} ${90 - Math.atan((cir2_config.x - cir1_config.x) / (cir2_config.y - cir1_config.y)) * (180 / Math.PI)} 0 ${curveDir()} ${cir2_config.x - cir1_config.x} ${cir2_config.y - cir1_config.y}`, //`M 0 ${-radius} A ${radius} ${radius} 0 0 1 0 ${radius}`,
          }}
        />
      {/if}

      <Image config={{ image }} />
    </Layer>
  </Stage>
</button>
<button on:click={cancel}>Cancel</button>
<!--<canvas id="myCanvas" on:mousemove={getMousePosition} style="background:url('News Recording.png')"-->
