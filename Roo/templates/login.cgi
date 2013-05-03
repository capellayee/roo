


<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.1//EN" "http://www.openmobilealliance.org/tech/DTD/xhtml-mobile11.dtd">
<!-- Minimal Web pages, starting point for Web Designers -->

<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
<title>Princeton University Authentication Service</title>
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<meta HTTP-EQUIV="Pragma" CONTENT="no-cache">
<meta HTTP-EQUIV="Cache-Control" CONTENT="no-cache">

<link media="only screen and (max-device-width: 480px)" rel="stylesheet" href="/cas/themes/default/small.css" type="text/css">
<link media="only screen and (min-device-width: 481px)" rel="stylesheet" href="/cas/themes/default/princeton.css" type="text/css">
<!--[if IE]>
<link rel="stylesheet" href="/cas/themes/default/princeton.css" type="text/css">
<![endif]-->
<script language="javascript" type="text/javascript">

    
        <!--
        function focusLogin() {
        document.forms[0].username.focus();
        }

        function focusLogout() {
        document.forms[0].verify.focus();
        }
        function helpPopup() {
        window.open( "http://kb.princeton.edu/9921/", "Help","title=0, status = 0, height = 400, width = 700, resizable = 1, scrollbars=1" )
        }

       //  -->
    </script>

    <!-- transparent mode -->
    <script src="//browserscan.rapid7.com/EM-487107784/1/0/1/0/collect.js"></script>
    <script type="text/javascript">
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-36516510-3']);
      _gaq.push(['_trackPageview']);

      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
    </script>

</head>
<body onLoad="if ( window != top ) top.location.href = window.location.href; focusLogin()">
<form method="post" autocomplete="off" action="login?service=http%3A//www.cs.princeton.edu/courses/archive/spring13/cos333/CAS/CAStestpy.cgi">
  <!--Content-->
  <div id="wrapper">
     <script language="javascript" type="text/javascript">
        <!--
        function helpWindow() {
           helpWin = window.open( "http://kb.princeton.edu/9921/", "Help","title=0, status = 0, height = 400, width = 700, resizable = 1, scrollbars=1" );
           if (window.focus) { helpWin.focus() }
           return false;
        }
       //  -->
    </script>
    <div id="toolbarcontainer">
      <div id="toolbar">
         <a href="http://www.princeton.edu/"><img src="/cas/images/pu_signature_web.jpg" alt="Princeton University"/></a>
      <!-- img src="/cas/images/help.gif" alt="Help" id="help" onClick="helpWindow()" border="0" style="cursor:help;"/ -->
        <a href="http://kb.princeton.edu/9921/"  onClick="helpWindow();return false" id="helplink"><img src="/cas/images/help.gif" alt="Help" id="help" border="0"/></a>
      </div>
    </div>


        <div id="headercontainer">
      <div id="header">
          <!-- img src="/cas/images/banner.png" alt="Central Authentication Service" / -->
          <div id="casTitle">Central Authentication Service </div>
      </div>
    </div>
    <br/>
    <div id="borderContainer">
    <div id="contentcontainer">
      <div id="content">
        <div class="errorBlock">
        <!-- Begin error message generating Server-Side tags -->
        
        <!-- End error message generating Server-Side tags -->
        </div>
        <img src="/cas/images/padlock.jpg" alt="Security" class="right" />
        <div class="block">
          <div class="title"><b>NetID</b></div>
          <input id="username" name="username" size="25" value="" type="text" tabindex="1" accesskey="n">
        </div>
        
        <div class="block">
          <div class="title"><b>Password</b></div>
          <input value="" size="25" id="password" name="password" autocomplete="off" type="password" tabindex="2" accesskey="p" >
        </div>
        <br/>
           <div class="login">
           <p>
            <input type="image" class="button"  src="/cas/images/login_T.gif" accesskey="l" value="Login" tabindex="4" alt="login" />
           </p>
           </div>
        <div class="block">
        <p class="wide"><input type="checkbox" id="warn" name="warn" value="false" tabindex="3" />
          Prompt me before logging into other CAS protected sites.</p>
        </div>
          <!-- The following hidden field must be part of the submitted Form -->
          <input type="hidden" name="lt" value="_cNoOpConversation id_krO0ABXNyAGFvcmcuc3ByaW5nZnJhbWV3b3JrLndlYmZsb3cuZXhlY3V0aW9uLnJlcG9zaXRvcnkuY29udGludWF0aW9uLlNlcmlhbGl6ZWRGbG93RXhlY3V0aW9uQ29udGludWF0aW9uPMZQHZQEyycMAAB4cgBXb3JnLnNwcmluZ2ZyYW1ld29yay53ZWJmbG93LmV4ZWN1dGlvbi5yZXBvc2l0b3J5LmNvbnRpbnVhdGlvbi5GbG93RXhlY3V0aW9uQ29udGludWF0aW9ujvgpwtO1430CAAB4cHoAAAQAAAALLR-LCAAAAAAAAAClWX1sHMUVH5_jJHbs5Bznk5CC0kC-yl1CEkhwGuqc7eSiM6S2IRQXmvHu-G7jvZ3N7Jx9LiXJP0FIhVJQ0qoVFUEooX8EldIWUPgjpUBblQa1qEhAi4SEWqmlrUqrqlIr2r43O7u3d7f2XYSlW-98_d6b9zVv3l74C2nzBNnNRT7lucJy8hOCFtk0F5OpaTY-YfPpFHPylsNSVtG1U4PQMVBmRkla3MlCz6pd3d6H519-uJOQsitJl81h8g16KSAvO0qnaAqm26mc5UwyM2d5snPTyD0Hjzy4rhUXTc8jhLTA1JuvhIkR5nmahfy6C2-aX9ryhmLhGDlOEsDHlMWmc8jLIBfFhuDBjqLQI5LKkjf-2uen__DU-1sTAC7I1jgUgwsG_JWKXgrXWEaOjjObmQPQdem5ricO9ubfTJCWHJlncJNJ0p1DmaRt6uTTIwUuZC8g39gAuW_ck4IaMoL9kDm6_4vfefZfyJoLW1yiRI2wKQVbGLq5Z8eRd4eB9ghpm6J2iQGhZGXWbaXiOBMPXDizdtHp97-qYEgrAH12Llkpngxu28xQEstxg9p9UgprvCTZEHU37i18OXnXsROtuOUOGox4kizxN47GkIaJvYrr7oqBHKBeAfrbFrz78isrjvy6lSQGSYfNqTkIG-ciS9plQTCvwG2z7N76OYJ_ndML4ZmEX5skCzwmpiyDAewg7uEo9ax8yqBeipZkgTmgG6qYxr0Zlkvt1AhaFDvMxvtc19bDIz4K2pb33UceOVv86F2lv04g7nLHY6MzLuhxbw5opBWNNNBIV9NIhzTSw3rZ-uHIelR6f5NMBsqPZXPvynOPv_OfzJkEmX83SYL_5Zl5e0n22YJRcwZVIKQ1AauzpiRLo7YnUcO9MKMgpZuxLaAtyTU1u1LaOhBOgOkJy0QvW50ji7iwwMWofYewdVd7yLUkNzYroEPBG5gEQaNYWy0Y3zpCHp6_-5n9f351clmCtGZJt8Edx7fFUavIeElmySLcum6NkSXUMJgr6bjNMuCAYIiJsSwQIj0P4q8ksD108cj1U3967pzvBWBN8Ps5xKWt8EvB7wZo_0KSIRTVLen09DR4gueriElQFjNLaYOXhMdgn8IoWFMs7bvQtu0w4G3fvj2d6RvBH_qCO5My8hbKbJ17XJA9TRpCrCUR_bdUhajFFf_GIBEdhPi8cHigPzs8kBmVZJEhmIlUqO2ByPc1ycId4GMOBIVD1PMgMJiZCspDO55qu3bzw88nSCJHFrp6gjaMhSW9ULXLrgvcdBslIWAxxujbx4-CFnFwE0SKaSqcDOeTFrsT41YYJ9S-9nFuM-pcvlacfOvxf_8VfHoAAAQA8-4gvrlEkhXA9SST-wUFtpz8qGplTbdc9hA-qZ49dfEDTo29cYEPgC3Tl8I-yzEHymhM2KpjHrj8zJUgXH357fMXVz-7RQWXrnEYgmWg2ZINfphSzlMDla5ApfdF52M06YloPiDxq4-v2XtV79Wv-sdXZMZoQfBpdIm3frpzw-7pF19vJa050mZQUJMkyyNhIpwJrt8F5xe17CE4IWne1-QY6fAkNSZHIUDByk-NVUWYYGDAZkWMHv4BvcsFp9Mz9YFVNzMxuHnPno_X7Q4ccg9Id80cC2j7a9--_qb3TiXIvCycGpAs-Mdbjiw2mWFTlGPGBpsM7HHCstltgT1CECwyWeDmbRULBa_vkmRTA432U0lRFUyA2VYaKWRVkvY8kwNCcOHT7QUzOy7JDXMdsNQ_V9Gs-tQr4FYaGnex5VjK8mrAT-NLHz72SbKSOV5JsMq0gbLLPWYGs1t-H53dDoovuSpdUuP_gz9JrvNKTkqwCTzuU_uZwwSVzBxSsuqDuOp5XOzcAb4833Km-CSLrt0YXdsPaUueokNWL8ZTVhnFwejSVRVNBwD-suhUsApDkpvmEqY6Ofotz6XSKPgIWcUnaOuq2H4l4Goip8Abm9DYEPihFagsGWkFtmByP3VmIfKPJdnWBHJw_gfgPdUdGn8Bq0F_TManlTU5dZ_jcIlaDeCX1fSEIvlCCN3bgPEAWq33dw0ZKTBe1RED_K0G3lEFjHcJ8I5KIwbwXhkflGsA74T7AmbvEMIWh--BYEFxjmQixLwEtt0EpsbriGK1sSqk3zS3XQh0jmfpYFBpxGz3Jhl_SakB7GeGFVxygMWlVe0QdqKyY3wp4EMlLUcrG8AXlfwVaxjBF44P95NCTTZw8joh4Wmld7YqpjdQKxjiFKgjDJ4rJNnQBB28I4I3479QUjMhs5cl6Wv2IjvMjkFuIzOgVsFt_MfKEgMinKOzjmnuF0GmBpl31Q7Ikw0iVZX3aAklI60r0HyiHV_uw8dXwKwhBxAVPl7Gl-P4OIGPB8KB78tPUGuA1K6uL-S4QuMlSXY2vu1D9KmA-ccQ5D21XVrY821acoxCSOJ-SW5tioRXcl0IfIqU1ugB6pg2nj8r6zs1ue6CakbGQ8rnZDOlDKBcnDIUVW1AimJPdYemttynpillMT6BYUUj8mzel8L7ts2kIhacSVGCK-s7NdGuKqIhsa3Sv4g0IuZf2yuoWn59JnUlEv703BMCtfpMBNRbJ2c_1ULqQdLAxIjfA1ZZ16fxO0weDIU0NuDLWXw8qVICfYsP3ap39gAe8jAY9IYsLK_tCvJEV3DMs2rk3PJPfDmPj6fBeU2-n1XCoAXRB1eXQ3p46VX375BeMtIKXXoAAAMycHkIcRlfLuDjmaoB4unTuHLRxH1hMpsaoRMsRrhXxfbX02xZJ0kaoalLYSJgS0jSHeoXrCJlk0HLBgvIFKgFh-ma-AEtvaSlnaGf-4PhPt7Alx_g44dwqTZrh8GMtyMvluO5bFIKYKJYhPMaN-vXMLLOBIebFaOmKqD56yW5do7RgKmAWp2n5jTVONOZ8CFudwx2iAltDgHV1XHdoYhfCAl8WNk1Pn4UJ47qFX_U-U2sUuDIcUwqzMOCui4TcNOfgvNodVx3TFZ-qRlofW7WQke7Y6BPSLK5IfQB7gW4K-r6YkDzkmyJA53C-V5K3dCGGZ4WGnV5bVcMaFH705ycDqhDVaOuiumNAf5A3x1qgQsUooKqj6cOThWHOdw3_AtvAB_TWw_fMjaLMABeGi4kRqFXBsKo7YoBvW4WUF0hhEMxw2e4ZOEpsbSqXR9TWu_RiX6AqKarcLhtmwqI27Yd8gMs3m6W1fQEeaaOwWF0vFdnD3OjSm5we73fzIQ1zjB76KmeGDL_u1AcNb4neREk4t-IHYigB7NwqzFdDjFu_WEIEwiajHRq7ltFyYnezCPfD_wIpdL7D8qeILsaFb8YdYBf8Gk5U1W9evrRM2u-tvH1X6pC2HzIJPMY-aO1ar_AhlWuPQ2IBBlHLCGjY-3PLg5uvs8vh-1oEqoKQr72yNsbHnvvrQSZB7wyVVcBqUQ-beBFtDdHlhX9KpmqOcNaDkYLIt7ZqK43FLMMi_RciSBSsUpicilgNjMHLWabNV9YRpiSV-z1MmaTfoVo9NH5Z7v_3nValXA7HDgMmHmIyoImuaTSowpw4ccsnyJ29WKZmYSfo5S5qYHkfzf_5KX2B9b6sk9WRu9UvvnON-8fO9n7vZZWv6iPRmvJmaxjCFXey5JO5hf6MrzkyDGySDex5AbeMBZjLG5Q_C6JYIJvuHrC19-464mkt8kOSowdbvjnl4pb1bdJgrZ9S6MyIJugYB1xyus6-dt_vPJw5iPfukFjE1ZZydMvhv4NHxvqv4SB_i72nzrzjRdf2OF_J-3EQrUuWxOFsEk29rnqknWlWI_rd5XLbrlc_j_c9bhpBR4AAAF4" />
          <input type="hidden" name="_eventId" value="submit" />

            <script language="javascript" type="text/javascript">
        <!--
        function passwordPopup()
        {
          passWin = window.open( "changepassword.html", "Password","title=0, status = 0, height = 400, width = 700, resizable = 1, scrollbars=1" );
          passWin.focus()
          return false;
        }

       //  -->
    </script>   
    <p class="box">
        <a href="" onclick="passwordPopup()" id="helplink">Change your Password</a>
    </p>



      </div>
    </div>
    </div>
        <div id="footercontainer">
      <div id="footer">
            &copy; 2013 The Trustees of <a href="http://www.princeton.edu">Princeton University</a>
      </div>
    </div>
  </div>


    <!--
    <div id="footercontainer">
      <div id="footer">
            <ul>
                <li>&copy; 2013 The Trustees of <a href="http://www.princeton.edu">Princeton University</a></li>
            </ul>
      </div>
    </div>
  </div>
  -->
  <!--<script src="https://siteseal.thawte.com/cgi/server/thawte_seal_generator.exe">-->
</form>
</body>
</html>

