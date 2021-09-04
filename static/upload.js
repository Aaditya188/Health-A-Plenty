/* If you are using webpack, do make sure to use import for jQuery, jQueryui and lodash */

/* widget simulates upload using promises, the actual ajax function for upload the user has to write */

(() => {
  $.widget('wgt.imageUploader', {
    _currentId: 0,
    _$template: Handlebars.compile(`<li image-idx="{{imageid}}">
        <img src="{{imageurl}}" />
        <span class="image-remove fa fa-times-circle"></span>
        <span class="image-size">{{imagesize}}</span>
      </li>`),
    _fileList: [],
    _$fileCtrl: $('<input type="file" accept="image/*" multiple />'),

    _calculateSize: sizeinBytes => {
      return sizeinBytes >= 1048576 ? `${(sizeinBytes / 1048576).toFixed(2)} Mb` :
      sizeinBytes >= 1024 ?
      `${(sizeinBytes / 1024).toFixed(2)} Kb` :
      `${sizeinBytes} bytes`;
    },

    _progressncount: function () {
      let totalSize = _.sumBy(this._fileList, fl => fl.file.size);
      let sizePercentage = Math.ceil(totalSize / this.options.maxSize * 100);
      if (sizePercentage <= 100) {
        if (sizePercentage <= 80) {
          $('.progress-bar', $(this.element)).removeClass('bg-danger').addClass('bg-info').css({ width: `${sizePercentage}%` });
        } else
        {
          $('.progress-bar', $(this.element)).removeClass('bg-info').addClass('bg-danger').css({ width: `${sizePercentage}%` });
        }
      } else
      {
        $('.progress-bar', $(this.element)).removeClass('bg-info').addClass('bg-danger').css({ width: '100%' });
      }

      if (this._fileList.length > 0) {
        $('.image-count', $(this.element)).html(this._fileList.length);
        $('.image-tot-size', $(this.element)).html(this._calculateSize(totalSize));
        $('.upload-start,.upload-clean', $(this.element)).removeAttr('disabled');
      } else
      {
        $('.image-count', $(this.element)).html('0');
        $('.image-tot-size', $(this.element)).html('0 Mb');
        $('.upload-start,.upload-clean', $(this.element)).attr('disabled', '');
      }
    },

    _selectFiles: function (images) {
      if (images.length > 0) {
        let validFiles = _.filter(images, image => {
          return image.type.match('image.*');
        });
        let currIndex = this._currentId;
        this._fileList = this._fileList.concat(_.map(validFiles, vf => {return { imageid: this._currentId++, file: vf };}));
        _.forEach(validFiles, vf => {
          let $html = $(this._$template({ imageurl: URL.createObjectURL(vf), imagesize: this._calculateSize(vf.size), imageid: currIndex++ }));

          $('.image-remove', $html).click(e => {
            $(e.target).parents('li').addClass('to-remove');
            this._fileList = _.reject(this._fileList, f => {
              return f.imageid == $(e.target).parents('li').attr('image-idx');
            });
            this._progressncount();
            setTimeout(() => {
              $(e.target).parents('li').remove();
            }, 500);
          });
          this._progressncount();
          $('.images-to-upload ul', $(this.element)).append($html);
        });

      }
    },

    options: {
      maxSize: 26214400,
      startUpload: files => {
        console.log('Simulating upload... override with your method... inject it from outside');
      } },


    _create: function () {
      $('.image-upload', $(this.element)).click(e => {
        this._$fileCtrl.click();
        return false;
      });

      this._$fileCtrl.change(e => {
        this._selectFiles($(e.target)[0].files);
        $(e.target).val(null);
      });

      $('.max-size-limit', $(this.element)).html(`max size limit ${this._calculateSize(this.options.maxSize)}`);

      $('.upload-start', $(this.element)).click(e => {
        $('.images-to-upload li', $(this.element)).removeClass('upload-err').removeClass('upload-success');
        this.options.startUpload(this._fileList);
        return false;
      });

      $('.upload-clean', $(this.element)).click(e => {
        this.clean();
        return false;
      });
    },

    clean: function () {
      this._fileList = [];
      $('.images-to-upload li', $(this.element)).remove();
      this._progressncount();
    },

    updateStatus: function (errored) {
      this._fileList = _.reject(this._fileList, f => {
        return !_.some(errored, err => err.imageid == f.imageid);
      });

      _.each($('.images-to-upload li', $(this.element)), li => {
        let $li = $(li);
        if (_.some(this._fileList, f => f.imageid == $li.attr('image-idx'))) {
          $li.addClass('upload-err');
        } else
        {
          $li.addClass('upload-success');
        }

        $('.upload-success', $(this.element)).remove();
        this._progressncount();
      });
    },

    _destroy: function () {
    } });



  // calling widget on div
  $('#imageWgt').imageUploader({
    startUpload: files => {
      //simulate errored files
      let errored = _.reject(files, f => f.imageid % 2 == 0);
      setTimeout(() => {
        $('#imageWgt').imageUploader('updateStatus', errored);
      }, 2000);
    } });

})();