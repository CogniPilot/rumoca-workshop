// Retry transient release-server failures without retrying permanent HTTP errors.
// Callers still verify the downloaded artifact against its pinned SHA256.
export async function downloadRelease(url) {
 for (let attempt=0; attempt<5; attempt++) {
  try {
   const response=await fetch(url,{signal:AbortSignal.timeout(90000)});
   if (!response.ok) {
    await response.body?.cancel();
    const error=new Error(`Release download failed: HTTP ${response.status}`);
    error.permanent=response.status<500 && response.status!==429;
    throw error;
   }
   return Buffer.from(await response.arrayBuffer());
  } catch (error) {
   if (error.permanent || attempt===4) throw error;
   const delay=1000*2**attempt;
   console.warn(`Release download attempt ${attempt+1} failed: ${error.message}; retrying in ${delay} ms`);
   await new Promise(resolve=>setTimeout(resolve,delay));
  }
 }
}
