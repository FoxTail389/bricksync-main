<script lang="ts">
  var pointy: number;
  var pointx: number;
  function equation() {
    // @ts-ignore
    var Expression = algebra.Expression;
    // @ts-ignore
    var Equation = algebra.Equation;
    var x = new Expression("x");
    var y = new Expression("y");
    var mousex = 421;
    var mousey = 320;
    var mx = 392; //new Expression("x1");
    var my = 265; //new Expression("y1");
    var x2 = 417; //new Expression("x2");
    var y2 = 264; //new Expression("y2");
    var eq1 = new Equation(
      x.subtract(mx).multiply(x2 - mx),
      y.subtract(my).multiply(my - y2)
    );
    var mouseeq = new Equation(
      x.subtract(mousex).multiply(y2 - my),
      y.subtract(mousey).multiply(x2 - mx)
    );
    var xeq;
    var yeq
    try {
      var asy = eq1.solveFor("y");
      try {
        var asx = eq1.solveFor("x")
        var solveforx = new Equation(
          asy,
          mouseeq.solveFor("y")
        )
        xeq = solveforx.solveFor('x')
        var solvefory=new Equation(
          asx,
          xeq
        )
        yeq= solvefory.solveFor("y")
      } catch (err1) {
        yeq=asy
        xeq=mouseeq.solveFor("x"); 
      }
    } catch (err) {
      xeq = eq1.solveFor("x");
      yeq = mouseeq.solveFor("y");
    }
    pointx = Math.round(xeq["numer"] / xeq["denom"]);
    pointy = Math.round(yeq["numer"] / yeq["denom"]);
  }
</script>

<svelte:head>
  <script async src="algebra-0.2.6.min.js" on:load={equation}></script>
</svelte:head>
<p>({pointx},{pointy})</p>
