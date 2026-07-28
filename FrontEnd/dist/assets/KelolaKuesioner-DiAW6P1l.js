import{a as w,s as H,b as I}from"./index-Cb5-83-5.js";import{B as K,a2 as j,g as A,o as v,c as V,a as t,m as P,i as G,_ as M,N as R,a0 as W,z as q,M as S,t as h,P as _,Q as J,h as u,w as b,A as d,a1 as Q,H as m,W as z,J as y,E as f,k as F,e as X}from"./index-BED9dlrk.js";import{s as Y}from"./index-CvN7bBze.js";import{s as N}from"./index-D3p1IG-s.js";import"./index-CcQ4q_rH.js";import"./index-RUZLvLaI.js";var Z=`
    .p-toggleswitch {
        display: inline-block;
        width: dt('toggleswitch.width');
        height: dt('toggleswitch.height');
    }

    .p-toggleswitch-input {
        cursor: pointer;
        appearance: none;
        position: absolute;
        top: 0;
        inset-inline-start: 0;
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
        opacity: 0;
        z-index: 1;
        outline: 0 none;
        border-radius: dt('toggleswitch.border.radius');
    }

    .p-toggleswitch-slider {
        cursor: pointer;
        width: 100%;
        height: 100%;
        border-width: dt('toggleswitch.border.width');
        border-style: solid;
        border-color: dt('toggleswitch.border.color');
        background: dt('toggleswitch.background');
        transition:
            background dt('toggleswitch.transition.duration'),
            color dt('toggleswitch.transition.duration'),
            border-color dt('toggleswitch.transition.duration'),
            outline-color dt('toggleswitch.transition.duration'),
            box-shadow dt('toggleswitch.transition.duration');
        border-radius: dt('toggleswitch.border.radius');
        outline-color: transparent;
        box-shadow: dt('toggleswitch.shadow');
    }

    .p-toggleswitch-handle {
        position: absolute;
        top: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: dt('toggleswitch.handle.background');
        color: dt('toggleswitch.handle.color');
        width: dt('toggleswitch.handle.size');
        height: dt('toggleswitch.handle.size');
        inset-inline-start: dt('toggleswitch.gap');
        margin-block-start: calc(-1 * calc(dt('toggleswitch.handle.size') / 2));
        border-radius: dt('toggleswitch.handle.border.radius');
        transition:
            background dt('toggleswitch.transition.duration'),
            color dt('toggleswitch.transition.duration'),
            inset-inline-start dt('toggleswitch.slide.duration'),
            box-shadow dt('toggleswitch.slide.duration');
    }

    .p-toggleswitch.p-toggleswitch-checked .p-toggleswitch-slider {
        background: dt('toggleswitch.checked.background');
        border-color: dt('toggleswitch.checked.border.color');
    }

    .p-toggleswitch.p-toggleswitch-checked .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.checked.background');
        color: dt('toggleswitch.handle.checked.color');
        inset-inline-start: calc(dt('toggleswitch.width') - calc(dt('toggleswitch.handle.size') + dt('toggleswitch.gap')));
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover) .p-toggleswitch-slider {
        background: dt('toggleswitch.hover.background');
        border-color: dt('toggleswitch.hover.border.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover) .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.hover.background');
        color: dt('toggleswitch.handle.hover.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover).p-toggleswitch-checked .p-toggleswitch-slider {
        background: dt('toggleswitch.checked.hover.background');
        border-color: dt('toggleswitch.checked.hover.border.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover).p-toggleswitch-checked .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.checked.hover.background');
        color: dt('toggleswitch.handle.checked.hover.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:focus-visible) .p-toggleswitch-slider {
        box-shadow: dt('toggleswitch.focus.ring.shadow');
        outline: dt('toggleswitch.focus.ring.width') dt('toggleswitch.focus.ring.style') dt('toggleswitch.focus.ring.color');
        outline-offset: dt('toggleswitch.focus.ring.offset');
    }

    .p-toggleswitch.p-invalid > .p-toggleswitch-slider {
        border-color: dt('toggleswitch.invalid.border.color');
    }

    .p-toggleswitch.p-disabled {
        opacity: 1;
    }

    .p-toggleswitch.p-disabled .p-toggleswitch-slider {
        background: dt('toggleswitch.disabled.background');
    }

    .p-toggleswitch.p-disabled .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.disabled.background');
    }
`,ee={root:{position:"relative"}},te={root:function(n){var c=n.instance,g=n.props;return["p-toggleswitch p-component",{"p-toggleswitch-checked":c.checked,"p-disabled":g.disabled,"p-invalid":c.$invalid}]},input:"p-toggleswitch-input",slider:"p-toggleswitch-slider",handle:"p-toggleswitch-handle"},ae=K.extend({name:"toggleswitch",style:Z,classes:te,inlineStyles:ee}),ne={name:"BaseToggleSwitch",extends:j,props:{trueValue:{type:null,default:!0},falseValue:{type:null,default:!1},readonly:{type:Boolean,default:!1},tabindex:{type:Number,default:null},inputId:{type:String,default:null},inputClass:{type:[String,Object],default:null},inputStyle:{type:Object,default:null},ariaLabelledby:{type:String,default:null},ariaLabel:{type:String,default:null}},style:ae,provide:function(){return{$pcToggleSwitch:this,$parentInstance:this}}},B={name:"ToggleSwitch",extends:ne,inheritAttrs:!1,emits:["change","focus","blur"],methods:{getPTOptions:function(n){var c=n==="root"?this.ptmi:this.ptm;return c(n,{context:{checked:this.checked,disabled:this.disabled}})},onChange:function(n){if(!this.disabled&&!this.readonly){var c=this.checked?this.falseValue:this.trueValue;this.writeValue(c,n),this.$emit("change",n)}},onFocus:function(n){this.$emit("focus",n)},onBlur:function(n){var c,g;this.$emit("blur",n),(c=(g=this.formField).onBlur)===null||c===void 0||c.call(g,n)}},computed:{checked:function(){return this.d_value===this.trueValue},dataP:function(){return A({checked:this.checked,disabled:this.disabled,invalid:this.$invalid})}}},le=["data-p-checked","data-p-disabled","data-p"],ie=["id","checked","tabindex","disabled","readonly","aria-checked","aria-labelledby","aria-label","aria-invalid"],se=["data-p"],oe=["data-p"];function de(i,n,c,g,k,l){return v(),V("div",P({class:i.cx("root"),style:i.sx("root")},l.getPTOptions("root"),{"data-p-checked":l.checked,"data-p-disabled":i.disabled,"data-p":l.dataP}),[t("input",P({id:i.inputId,type:"checkbox",role:"switch",class:[i.cx("input"),i.inputClass],style:i.inputStyle,checked:l.checked,tabindex:i.tabindex,disabled:i.disabled,readonly:i.readonly,"aria-checked":l.checked,"aria-labelledby":i.ariaLabelledby,"aria-label":i.ariaLabel,"aria-invalid":i.invalid||void 0,onFocus:n[0]||(n[0]=function(){return l.onFocus&&l.onFocus.apply(l,arguments)}),onBlur:n[1]||(n[1]=function(){return l.onBlur&&l.onBlur.apply(l,arguments)}),onChange:n[2]||(n[2]=function(){return l.onChange&&l.onChange.apply(l,arguments)})},l.getPTOptions("input")),null,16,ie),t("div",P({class:i.cx("slider")},l.getPTOptions("slider"),{"data-p":l.dataP}),[t("div",P({class:i.cx("handle")},l.getPTOptions("handle"),{"data-p":l.dataP}),[G(i.$slots,"handle",{checked:l.checked})],16,oe)],16,se)],16,le)}B.render=de;const re={class:"stat-grid",style:{"margin-bottom":"18px"}},ue={class:"stat"},ce={class:"v"},ge={class:"stat"},he={class:"v",style:{color:"#16a34a"}},pe={class:"stat"},be={class:"v",style:{color:"#94a3b8"}},ve={class:"stat"},we={class:"v"},me={class:"kat-head"},ye={class:"kat-kode"},fe={class:"muted",style:{"font-weight":"400"}},ke={style:{display:"flex","align-items":"center",gap:"8px"}},xe={style:{display:"flex","flex-direction":"column",gap:"12px"}},Pe={class:"ro-field"},Ve={style:{display:"flex",gap:"12px"}},$e={style:{width:"120px"}},Se={style:{width:"120px"}},Be={style:{display:"flex","align-items":"center",gap:"10px"}},Ce={__name:"KelolaKuesioner",setup(i){const n=R(),c=W(),g=y([]),k=y(!0),l=y(!1),r=y({}),x=y(!1),C=z(()=>g.value.reduce((s,e)=>s+e.pertanyaan.filter(a=>a.aktif).length,0)),T=z(()=>g.value.reduce((s,e)=>s+e.pertanyaan.length,0));async function $(){k.value=!0;const{data:s}=await m.get("/master/kuesioner/manage");g.value=s,k.value=!1}function U(s){var e;x.value=!0,r.value={kategori_id:s.id,kategori_nama:`${s.kode}. ${s.nama}`,nomor:"",pertanyaan:"",urutan:(((e=s.pertanyaan.at(-1))==null?void 0:e.urutan)||0)+1,aktif:!0},l.value=!0}function D(s,e){x.value=!1,r.value={...e,kategori_nama:`${s.kode}. ${s.nama}`,aktif:!!e.aktif},l.value=!0}async function L(){var e,a;const s={kategori_id:r.value.kategori_id,nomor:r.value.nomor,pertanyaan:r.value.pertanyaan,urutan:r.value.urutan,aktif:r.value.aktif};try{x.value?await m.post("/master/kuesioner/pertanyaan",s):await m.put(`/master/kuesioner/pertanyaan/${r.value.id}`,s),l.value=!1,await $(),n.add({severity:"success",summary:"Pertanyaan tersimpan",life:1500})}catch(o){n.add({severity:"error",summary:"Gagal menyimpan",detail:(a=(e=o==null?void 0:o.response)==null?void 0:e.data)==null?void 0:a.detail,life:3500})}}async function O(s){var a,o;const e=!s.aktif;try{await m.put(`/master/kuesioner/pertanyaan/${s.id}`,{aktif:e}),s.aktif=e?1:0,n.add({severity:"success",summary:e?"Dipublish":"Di-unpublish",life:1200})}catch(p){n.add({severity:"error",summary:"Gagal",detail:(o=(a=p==null?void 0:p.response)==null?void 0:a.data)==null?void 0:o.detail,life:3e3})}}function E(s){c.require({message:`Hapus pertanyaan "${s.nomor||s.pertanyaan.slice(0,40)}"? Tindakan ini tidak bisa dibatalkan.`,header:"Hapus Pertanyaan",icon:"pi pi-exclamation-triangle",acceptClass:"p-button-danger",acceptLabel:"Hapus",rejectLabel:"Batal",accept:async()=>{var e,a;try{await m.delete(`/master/kuesioner/pertanyaan/${s.id}`),await $(),n.add({severity:"success",summary:"Pertanyaan dihapus",life:1500})}catch(o){n.add({severity:"warn",summary:"Tidak bisa dihapus",detail:(a=(e=o==null?void 0:o.response)==null?void 0:e.data)==null?void 0:a.detail,life:4e3})}}})}return q($),(s,e)=>(v(),V(_,null,[e[16]||(e[16]=t("p",{class:"muted",style:{"margin-top":"0"}},[S(" Kelola daftar pertanyaan kuesioner CEE. Hanya pertanyaan yang "),t("strong",null,"dipublish"),S(" (aktif) yang muncul di Survei Publik dan Form 1.a. ")],-1)),t("div",re,[t("div",ue,[t("div",ce,h(T.value),1),e[6]||(e[6]=t("div",{class:"l"},"Total Pertanyaan",-1))]),t("div",ge,[t("div",he,h(C.value),1),e[7]||(e[7]=t("div",{class:"l"},"Dipublish (Aktif)",-1))]),t("div",pe,[t("div",be,h(T.value-C.value),1),e[8]||(e[8]=t("div",{class:"l"},"Draft (Belum Dipublish)",-1))]),t("div",ve,[t("div",we,h(g.value.length),1),e[9]||(e[9]=t("div",{class:"l"},"Sub-unsur",-1))])]),(v(!0),V(_,null,J(g.value,a=>(v(),V("div",{key:a.id,class:"page-card",style:{"margin-bottom":"16px",padding:"0"}},[t("div",me,[t("div",null,[t("span",ye,h(a.kode),1),S(" "+h(a.nama)+" ",1),t("span",fe,"("+h(a.pertanyaan.filter(o=>o.aktif).length)+"/"+h(a.pertanyaan.length)+" dipublish)",1)]),u(d(f),{label:"Tambah",icon:"pi pi-plus",size:"small",outlined:"",onClick:o=>U(a)},null,8,["onClick"])]),u(d(H),{value:a.pertanyaan,loading:k.value,size:"small",stripedRows:""},{empty:b(()=>[...e[10]||(e[10]=[t("div",{class:"muted",style:{padding:"12px"}},"Belum ada pertanyaan pada sub-unsur ini.",-1)])]),default:b(()=>[u(d(w),{field:"nomor",header:"No",style:{width:"70px"}}),u(d(w),{field:"pertanyaan",header:"Pertanyaan",style:{minWidth:"340px"}}),u(d(w),{field:"urutan",header:"Urutan",style:{width:"80px"},bodyClass:"c"}),u(d(w),{header:"Publish",style:{width:"110px"}},{body:b(({data:o})=>[t("div",ke,[u(d(B),{modelValue:!!o.aktif,"onUpdate:modelValue":p=>O(o)},null,8,["modelValue","onUpdate:modelValue"]),o.aktif?(v(),F(d(N),{key:0,value:"Live",severity:"success"})):(v(),F(d(N),{key:1,value:"Draft",severity:"secondary"}))])]),_:1}),u(d(w),{header:"",style:{width:"96px"}},{body:b(({data:o})=>[u(d(f),{icon:"pi pi-pencil",text:"",rounded:"",size:"small",onClick:p=>D(a,o)},null,8,["onClick"]),u(d(f),{icon:"pi pi-trash",text:"",rounded:"",size:"small",severity:"danger",onClick:p=>E(o)},null,8,["onClick"])]),_:2},1024)]),_:2},1032,["value","loading"])]))),128)),u(d(Q),{visible:l.value,"onUpdate:visible":e[5]||(e[5]=a=>l.value=a),header:x.value?"Tambah Pertanyaan":"Edit Pertanyaan",modal:"",style:{width:"620px"}},{footer:b(()=>[u(d(f),{label:"Batal",text:"",onClick:e[4]||(e[4]=a=>l.value=!1)}),u(d(f),{label:"Simpan",icon:"pi pi-check",onClick:L})]),default:b(()=>[t("div",xe,[t("div",null,[e[11]||(e[11]=t("label",{class:"lbl muted"},"Sub-unsur",-1)),t("div",Pe,h(r.value.kategori_nama),1)]),t("div",Ve,[t("div",$e,[e[12]||(e[12]=t("label",{class:"lbl muted"},"Nomor",-1)),u(d(X),{modelValue:r.value.nomor,"onUpdate:modelValue":e[0]||(e[0]=a=>r.value.nomor=a),style:{width:"100%"},placeholder:"mis. 1"},null,8,["modelValue"])]),t("div",Se,[e[13]||(e[13]=t("label",{class:"lbl muted"},"Urutan",-1)),u(d(I),{modelValue:r.value.urutan,"onUpdate:modelValue":e[1]||(e[1]=a=>r.value.urutan=a),min:0,showButtons:"",style:{width:"100%"}},null,8,["modelValue"])])]),t("div",null,[e[14]||(e[14]=t("label",{class:"lbl muted"},"Teks Pertanyaan",-1)),u(d(Y),{modelValue:r.value.pertanyaan,"onUpdate:modelValue":e[2]||(e[2]=a=>r.value.pertanyaan=a),autoResize:"",rows:"3",style:{width:"100%"}},null,8,["modelValue"])]),t("div",Be,[u(d(B),{modelValue:r.value.aktif,"onUpdate:modelValue":e[3]||(e[3]=a=>r.value.aktif=a),inputId:"aktif-sw"},null,8,["modelValue"]),e[15]||(e[15]=t("label",{for:"aktif-sw"},"Publish (tampilkan di survei & Form 1.a)",-1))])])]),_:1},8,["visible","header"])],64))}},De=M(Ce,[["__scopeId","data-v-3dcc1fd8"]]);export{De as default};
