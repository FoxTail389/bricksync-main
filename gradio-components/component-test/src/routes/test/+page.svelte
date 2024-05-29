<script lang="ts">
    import { onMount } from "svelte";
  // @ts-ignore
  let state = 0;
  onMount(() => {
    const canvas = <HTMLCanvasElement>document.getElementById("myCanvas");
    const ctx = canvas.getContext("2d");
    const image: any = document.getElementById("image1");
    var newImg = new Image;
    newImg.onload = function() {
        newImg.src = "News Recording.png";
    }
    
    console.log(newImg.width)
    canvas.height=canvas.width*(image.naturalHeight/image.naturalWidth)
    image!.addEventListener("load", (e: any) => {
      ctx!.imageSmoothingEnabled = false;
      ctx!.drawImage(image,0,0, canvas.width, canvas.width * image.naturalHeight / image.naturalWidth);
    });
  });
  function getMousePosition(event: any) {
    let rect = event.target.getBoundingClientRect();
    const image = <HTMLImageElement>document.getElementById("myCanvas");
    const percent = event.target.width / image.naturalWidth;
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    return [Math.round(x / percent), Math.round(y / percent)];
  }
  // @ts-ignore
  function click(event) {
    console.log(getMousePosition(event));
  }
</script>

<button class="w-full" on:click={click} on:mousemove={(e) => console.log(getMousePosition(e))}>
  <img src="News Recording.png" id="image1" hidden alt="test">
  <canvas id="myCanvas" class="w-full">
   
  </canvas>
</button>